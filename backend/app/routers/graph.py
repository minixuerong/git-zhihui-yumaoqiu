"""图谱数据 API - 从数据库动态组装 ECharts 力导向图数据"""
import json
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models

router = APIRouter(prefix="/api/v1/graph", tags=["graph"])

ID_PREFIX_JOB = "job:"
ID_PREFIX_SKILL = "skill:"


def _load_original_graph():
    """读取原始 graph_data.json 获取节点样式基准值"""
    graph_path = os.path.join(
        os.path.dirname(__file__), '..', '..', '..',
        'frontend', 'src', 'assets', 'graph_data.json'
    )
    if not os.path.exists(graph_path):
        return {}, [], []
    with open(graph_path, encoding='utf-8') as f:
        data = json.load(f)

    orig_sizes = {}
    orig_job_nodes = []
    for n in data.get('nodes', []):
        if n.get('category') != 8:
            orig_sizes[n['name']] = {
                'symbolSize': n.get('symbolSize', 30),
                'value': n.get('value', 1),
                'category': n.get('category', 0)
            }
            orig_job_nodes.append(n['name'])

    return orig_sizes, data.get('jobSkills', {}), orig_job_nodes


def _match_job_group(db, graph_job_names):
    """将数据库中的岗位按 graph_data 的岗位名分组匹配"""
    all_jobs = db.query(models.Job).filter(
        models.Job.is_deleted == False
    ).all()

    # 先收集所有 exact 匹配的 job id，避免被 partial 抢走
    exact_claimed = set()
    groups = {}
    for name in graph_job_names:
        exact = [j for j in all_jobs if j.name.strip() == name]
        for j in exact:
            exact_claimed.add(j.id)
        groups[name] = {'exact': exact, 'partial': [], 'total': len(exact)}

    # 再算 partial，排除已被 exact 占用的
    for name in graph_job_names:
        partial = [
            j for j in all_jobs
            if name in j.name
            and j.name.strip() != name
            and j.id not in exact_claimed
        ]
        groups[name]['partial'] = partial
        groups[name]['total'] += len(partial)

    return groups


@router.get("/jobs")
def get_graph_jobs(db: Session = Depends(get_db)):
    """返回图谱中9个岗位及其DB ID（用于前端岗位下拉框）"""
    _, _, graph_job_names = _load_original_graph()
    job_groups = _match_job_group(db, graph_job_names)
    result = []
    for name in graph_job_names:
        info = job_groups.get(name, {})
        exact = info.get('exact', [])
        if exact:
            result.append({"id": exact[0].id, "name": name, "db_name": exact[0].name})
        else:
            partial = info.get('partial', [])
            if partial:
                partial.sort(key=lambda x: len(x.name))
                result.append({"id": partial[0].id, "name": name, "db_name": partial[0].name})
    return result


@router.get("/data")
def get_graph_data(db: Session = Depends(get_db)):
    """获取能力图谱数据"""

    orig_sizes, orig_job_skills, graph_job_names = _load_original_graph()
    job_groups = _match_job_group(db, graph_job_names)

    # ===== 1. 分类 =====
    categories_db = db.query(models.JobCategory).filter(
        models.JobCategory.is_deleted == False
    ).all()
    categories = [{"name": c.name, "description": c.description or ""} for c in categories_db]

    # ===== 2. 节点 =====
    # 技能被引用次数统计
    skill_usage = dict(
        db.query(
            models.CapabilityRequirement.skill_id,
            func.count(models.CapabilityRequirement.id)
        ).group_by(models.CapabilityRequirement.skill_id).all()
    )

    nodes = []

    # 构建 DB category_id → graph category index 映射
    skill_cat_id = None
    for c in categories_db:
        if c.name == "技能":
            skill_cat_id = c.id
            break

    def db_cat_to_graph_idx(db_cat_id):
        if db_cat_id == skill_cat_id:
            return 8
        return db_cat_id - 1

    # 岗位节点 — 使用 job: 前缀确保 id 唯一
    for name in graph_job_names:
        info = job_groups.get(name, {})
        total = info.get('total', 0)
        orig = orig_sizes.get(name, {'symbolSize': 40, 'value': 1, 'category': 0})
        db_cat = info.get('exact', [None])[0]
        cat_idx = db_cat_to_graph_idx(db_cat.category_id) if db_cat else orig.get('category', 0)
        nodes.append({
            "id": ID_PREFIX_JOB + name,
            "name": name,
            "category": cat_idx,
            "symbolSize": orig.get('symbolSize', 40),
            "value": orig.get('value', 1),
            "relatedJobs": total
        })

    # 技能节点 — 按名称去重，合并 usage 计数
    skills = db.query(models.Skill).filter(
        models.Skill.is_deleted == False
    ).all()

    # 按名称去重（保留首个，合并 usage）
    skill_groups = {}
    for s in skills:
        key = s.name
        if key not in skill_groups:
            skill_groups[key] = {"usage": 0, "id": s.id}
        skill_groups[key]["usage"] += skill_usage.get(s.id, 0)

    max_skill_usage = max(g["usage"] for g in skill_groups.values()) if skill_groups else 1

    for sname, sinfo in skill_groups.items():
        usage = sinfo["usage"]
        if usage == 0:
            continue
        size = 25 + int(usage / max_skill_usage * 20)
        nodes.append({
            "id": ID_PREFIX_SKILL + sname,
            "name": sname,
            "category": 8,
            "symbolSize": size if size >= 25 else 25,
            "value": usage,
            "categoryName": "技能"
        })

    # ===== 3. 关联边 =====
    links_data = db.query(
        models.CapabilityRequirement
    ).join(
        models.Job, models.CapabilityRequirement.job_id == models.Job.id
    ).join(
        models.Skill, models.CapabilityRequirement.skill_id == models.Skill.id
    ).filter(
        models.Job.is_deleted == False,
        models.Skill.is_deleted == False,
        models.CapabilityRequirement.importance_score >= 0.4
    ).all()

    # 构建 job_id → graph_job_name 映射
    job_id_to_graph_name = {}
    for graph_name, info in job_groups.items():
        for j in info.get('exact', []):
            job_id_to_graph_name[j.id] = graph_name
        for j in info.get('partial', []):
            job_id_to_graph_name[j.id] = graph_name

    # 聚合边，source/target 使用带前缀的 id
    link_agg = {}
    for cr in links_data:
        graph_name = job_id_to_graph_name.get(cr.job_id)
        if not graph_name:
            continue
        skill = db.query(models.Skill).filter(models.Skill.id == cr.skill_id).first()
        if not skill:
            continue
        key = (ID_PREFIX_JOB + graph_name, ID_PREFIX_SKILL + skill.name)
        if key not in link_agg:
            link_agg[key] = {"value": 0, "count": 0, "jobName": graph_name, "skillName": skill.name}
        link_agg[key]["value"] += cr.importance_score or 0.2
        link_agg[key]["count"] += 1

    links = []
    for (source, target), info in link_agg.items():
        avg_value = info["value"] / info["count"]
        links.append({
            "source": source,
            "target": target,
            "jobName": info["jobName"],
            "skillName": info["skillName"],
            "value": round(avg_value * 5, 1),
            "confidence": round(0.5 + avg_value * 0.3, 2)
        })

    # ===== 4. jobSkills =====
    job_skills = {}
    for (source, target), info in link_agg.items():
        job_name = info["jobName"]
        if job_name not in job_skills:
            job_skills[job_name] = []
        avg_value = info["value"] / info["count"]
        job_skills[job_name].append({
            "name": info["skillName"],
            "importance": round(avg_value, 2),
            "count": info["count"]
        })

    # ===== 5. 分类统计 =====
    category_stats = []
    for c in categories_db:
        if c.name == "技能":
            continue
        graph_idx = db_cat_to_graph_idx(c.id)
        cat_jobs = [n["name"] for n in nodes if n.get("category") == graph_idx]
        cat_skills = set()
        for l in links:
            if l["jobName"] in cat_jobs:
                cat_skills.add(l["skillName"])
        category_stats.append({
            "name": c.name,
            "jobs": len(cat_jobs),
            "skills": len(cat_skills)
        })

    # ===== 6. Meta =====
    meta = {
        "totalNodes": len(nodes),
        "totalLinks": len(links),
        "totalCategories": len(categories),
        "generatedAt": db.query(func.now()).scalar().isoformat()
    }

    return {
        "categories": categories,
        "nodes": nodes,
        "links": links,
        "jobSkills": job_skills,
        "categoryStats": category_stats,
        "meta": meta
    }
