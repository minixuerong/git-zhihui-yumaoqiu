<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="bg-pattern"></div>
    <div class="network-grid"></div>

    <!-- 顶部导航 -->
    <header class="header">
      <div class="logo">
        <div class="logo-icon">CB</div>
        <span class="logo-text">CAPABILITY<span class="logo-dot">.</span>BRAIN</span>
      </div>
      <nav class="nav-links">
        <a href="javascript:void(0)" class="nav-link" @click="showSection = 'features'">产品功能</a>
        <a href="javascript:void(0)" class="nav-link" @click="showSection = 'solutions'">解决方案</a>
        <a href="javascript:void(0)" class="nav-link" @click="showSection = 'docs'">文档中心</a>
        <a href="javascript:void(0)" class="nav-link" @click="showSection = 'about'">关于我们</a>
      </nav>
    </header>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧 Hero -->
      <section class="hero-section">
        <h1 class="hero-title">
          人才能力<br>
          <span class="hero-highlight">智能引擎</span>
        </h1>
        <p class="hero-desc">
          基于大模型与知识图谱技术，构建新一代人才能力分析平台。
          实时感知岗位技能演变，精准匹配人才与岗位，助力数字经济时代的人才战略升级。
        </p>
        <div class="hero-stats">
          <div class="hero-stat">
            <div class="hero-stat-value">1,284</div>
            <div class="hero-stat-label">岗位覆盖</div>
          </div>
          <div class="hero-stat">
            <div class="hero-stat-value">8,542</div>
            <div class="hero-stat-label">技能节点</div>
          </div>
          <div class="hero-stat">
            <div class="hero-stat-value">94%</div>
            <div class="hero-stat-label">解析准确率</div>
          </div>
        </div>
      </section>

      <!-- 右侧登录 -->
      <section class="login-section">
        <div class="login-card">
          <div v-if="errorMsg" class="error-message show">{{ errorMsg }}</div>

          <h2 class="login-title">登录系统</h2>
          <p class="login-subtitle">欢迎使用人才能力大脑</p>

          <el-form
            ref="formRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            @submit.prevent="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                :prefix-icon="User"
                size="large"
                class="custom-input"
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                :prefix-icon="Lock"
                size="large"
                show-password
                class="custom-input"
              />
            </el-form-item>

            <div class="form-options">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <a href="javascript:void(0)" class="forgot-link">忘记密码</a>
            </div>

            <el-button
              type="primary"
              size="large"
              class="login-btn"
              :loading="loading"
              native-type="submit"
            >
              登录
            </el-button>
          </el-form>

          <p class="signup-link">
            还没有账号? <a href="javascript:void(0)" @click="registerDialogVisible = true">立即注册</a>
          </p>
        </div>
      </section>
    </div>

    <!-- 管理员通道弹窗 -->
    <el-dialog v-model="adminDialogVisible" title="管理员通道" width="400px" :close-on-click-modal="false">
      <el-form ref="adminFormRef" :model="adminForm" :rules="adminRules" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="adminForm.username" placeholder="管理员账号" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="adminForm.password" type="password" placeholder="管理员密码" :prefix-icon="Lock" size="large" show-password @keyup.enter="handleAdminLogin" />
        </el-form-item>
        <p v-if="adminError" class="admin-error">{{ adminError }}</p>
      </el-form>
      <template #footer>
        <el-button @click="adminDialogVisible = false; adminError = ''">取消</el-button>
        <el-button type="primary" @click="handleAdminLogin" :loading="adminLoading">验证</el-button>
      </template>
    </el-dialog>

    <!-- 注册弹窗 -->
    <el-dialog v-model="registerDialogVisible" title="注册账号" width="420px" :close-on-click-modal="false">
      <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="registerForm.username" placeholder="用户名（至少3位）" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="密码（至少6位）" :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="确认密码" :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item prop="role" style="margin-bottom: 0;">
          <el-radio-group v-model="registerForm.role" class="role-selector">
            <el-radio value="user" size="large">
              <div class="role-option">
                <span class="role-label">求职者</span>
                <span class="role-desc">浏览岗位、上传简历、匹配分析</span>
              </div>
            </el-radio>
            <el-radio value="hr" size="large">
              <div class="role-option">
                <span class="role-label">招聘者</span>
                <span class="role-desc">发布岗位、管理招聘、筛选简历</span>
              </div>
            </el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="registerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRegister" :loading="registerLoading">注册</el-button>
      </template>
    </el-dialog>

    <!-- ===== 产品功能弹窗 ===== -->
    <el-dialog :model-value="showSection === 'features'" title="产品功能" width="780px" top="5vh" @close="showSection = ''" destroy-on-close>
      <div class="section-modal">
        <h4 class="section-chapter">一、能力图谱引擎</h4>
        <p>能力图谱是平台的核心基础设施，以知识图谱技术为底座，构建了覆盖多行业、多层级的人才能力知识网络。图谱引擎通过对海量岗位数据、技能数据、行业报告的深度挖掘与语义分析，自动提取并结构化岗位所需的核心能力要素，形成从"行业—领域—岗位—技能—知识"的五级能力体系。每个能力节点关联其前置技能、进阶路径与实际应用场景，支持按技术栈、职级体系、行业分类等多维度进行切换与钻取。图谱引擎不仅展示能力的静态结构，还融合了实时态势感知模块，通过全网数据采集与分析，自动追踪新兴技能的出现、技能热度的波动以及岗位需求的变化趋势，为个人与组织提供动态的能力更新指引。</p>
        <p>图谱引擎的智能化体现在其持续学习与自适应更新机制上。系统集成了自然语言处理与机器学习模型，能够自动从互联网招聘信息、行业白皮书、专业论坛等多元数据源中抽取技能与岗位关联信息，经过语义对齐与冲突消解后动态更新现有图谱节点。对于尚未纳入体系的新兴能力，引擎会启动自动识别与提案机制，生成初步的技术定义与关联分析，供领域专家审核确认。这种"机器采集—自动构建—人工校验"的闭环模式，确保了图谱始终保持前沿性与准确性。截至目前，图谱引擎已涵盖超过1,200个标准化岗位定义、8,500余个技能节点以及30万余条能力关联关系，覆盖信息技术、金融服务、先进制造等五大核心行业领域。</p>

        <h4 class="section-chapter">二、智能岗位发现</h4>
        <p>智能岗位发现模块重新定义了岗位管理与更新的工作范式。传统的岗位定义往往依赖人力资源从业者的经验积累，存在标准化程度低、更新周期长、与市场脱节等痛点。该模块通过分布式爬虫系统实时采集主流招聘平台、企业官网、行业论坛等公开数据，结合预训练语言模型进行岗位实体的智能识别与规范化处理。系统能够自动判别岗位信息中的关键字段——包括岗位名称、职责描述、任职要求、薪资范围、技能标签等——并将其映射到标准化岗位库中。对于全新出现的岗位类型，系统会基于语义相似度与聚类分析算法，自动生成候选岗位定义草案，涵盖典型职责描述、核心技能要求、相似岗位对比以及演变趋势分析。</p>
        <p>岗位发现模块同时具备数据清洗与质量管控能力。原始采集数据中不可避免存在重复发布、信息缺失、格式不统一等噪声问题。系统内置了多层数据清洗管道，依次执行去重校验、字段补全、格式标准化以及语义一致性检查等操作。清洗后的数据进入人工审核工作台，支持操作员以标签化、卡片化的交互方式快速审阅与确认。审核通过的数据最终进入已发布岗位库，同步推送至用户端"岗位发现"模块进行展示。整个流程从数据采集到发布上线通常在分钟级内完成，大幅提升了岗位数据的时效性与可用性。同时，系统对每次数据变更保留完整审计日志，确保所有操作可追溯、可回滚。</p>

        <h4 class="section-chapter">三、人岗匹配分析</h4>
        <p>人岗匹配分析是实现精准推荐的核心环节。系统采用多阶段融合策略，综合运用传统规则引擎与大型语言模型，从多个维度对人岗匹配度进行深度评估。第一阶段为基于知识图谱的结构化匹配，系统将个人简历中的能力标签与岗位要求进行体系化对齐，计算技能覆盖度、技能深度匹配率以及能力差距指数，生成结构化的匹配报告。第二阶段引入大语言模型进行语义理解与上下文感知分析，突破传统关键词匹配的局限，能够理解简历与岗位描述中的深层语义关联——例如，在招聘要求中提及"微服务架构"与简历中出现"Spring Cloud"均可被识别为高相关性能力指标。</p>
        <p>匹配分析输出不仅包含综合匹配得分，还提供详尽的差距分析与改进建议。差距分析模块基于能力图谱的等级体系，精准定位个人能力与岗位要求之间的技能缺口，按严重程度划分为"缺失""不足""达标""超越"四个等级，并结合岗位的实际权重给出差异化的优先级排序。改进建议模块则根据识别出的能力差距，从学习与发展角度提供针对性的行动方案——包括推荐具体的学习课程、实践项目、专业书籍以及认证考试路径。每一份匹配报告均可导出为PDF格式，支持求职者用于个人简历优化，也可作为组织内部人才盘点的辅助工具。截至目前，匹配分析的语义解析准确率已达94%以上，显著优于传统关键词匹配方案。</p>

        <h4 class="section-chapter">四、学习路径规划</h4>
        <p>学习路径规划模块将能力图谱与个性化学习结合，为每一位用户提供定制化的成长路线图。系统首先通过对用户当前能力水平的评估（基于上传简历的自动解析结果或手动能力自评），确定用户在能力图谱中的起点位置。结合用户设定的职业发展目标——如目标岗位、期望职级、目标行业等——系统基于图谱中的能力演进关系与岗位能力要求，自动计算从当前状态到目标状态的最优学习路径。路径规划遵循"基础—进阶—高级—专家"的梯队设计原则，确保学习内容的合理递进与循序渐进。每条路径包含具体的技能目标、推荐学习资源、预期完成时间以及阶段性评估节点。</p>
        <p>学习路径的推荐算法融合了协同过滤与知识图谱推理两种技术路线。协同过滤层面，系统分析大量具有相似背景用户的学习行为数据与职业发展轨迹，挖掘高效的学习路径模式。知识图谱推理层面，系统基于能力节点之间的"前置依赖""层级归属""跨域映射"等语义关系，通过图神经网络模型计算不同学习顺序的有效性概率，优选出覆盖全面且效率最高的路径方案。除了自动规划外，用户也可以对系统推荐的学习路径进行手动调整——添加或删除技能目标、调整学习顺序、自定义学习资源等——系统会实时重新计算路径的完整性评估与预期效果。学习过程中，系统持续追踪用户的技能掌握度变化，动态调整后续学习内容，实现真正的自适应学习体验。</p>

        <h4 class="section-chapter">五、精准简历解析</h4>
        <p>简历解析引擎是系统与用户交互的重要入口之一。平台支持PDF、DOCX、DOC等多种常见简历格式的上传，解析引擎基于深度学习与自然语言处理技术，自动完成简历的结构化信息抽取。解析过程覆盖简历中的多个信息维度：个人信息（姓名、联系方式、教育背景）、工作经历（公司名称、职位、时间段、工作职责）、技能标签（编程语言、工具框架、专业能力）、项目经验（项目名称、角色、技术栈、成果描述）以及证书与荣誉等。引擎采用自底向上的解析策略，先识别页面中的文本区块与版面结构，再进行字段级的信息分类与语义提取，最后通过实体链接与归一化处理将抽取内容映射到标准化知识库中。</p>
        <p>为应对不同模板与表述风格带来的解析挑战，引擎融合了规则基与模型基的双重策略。对于格式规范的简历，基于模板匹配的快速解析通道能够在秒级内完成结构提取；对于格式复杂或表述模糊的简历，系统自动切换至深度语义分析模式，调用预训练语言模型进行细粒度的信息抽取与消歧。抽取完成后，系统会进行完整性校验与置信度评分，对低置信度字段标记提示供用户手动校正。所有解析历史将被保留并与用户账号绑定，支持多次上传后的增量更新与版本回溯。在企业场景下，批量解析功能可一次性处理数百份简历，并自动完成去重、分类与初步筛选流程，极大提升了招聘流程前端的效率。</p>
      </div>
    </el-dialog>

    <!-- ===== 解决方案弹窗 ===== -->
    <el-dialog :model-value="showSection === 'solutions'" title="解决方案" width="780px" top="5vh" @close="showSection = ''" destroy-on-close>
      <div class="section-modal">
        <h4 class="section-chapter">一、企业人才发展解决方案</h4>
        <p>面向中大型企业的人力资源部门与人才发展中心，平台提供端到端的人才能力管理数字化方案。方案涵盖岗位能力模型构建、人才盘点与继任规划、个性化培训推荐以及内部人才流动匹配四大核心场景。通过接入企业内部岗位体系与组织架构数据，平台自动为企业构建专属的能力图谱，将企业特有的岗位定义、职级体系、能力评估标准与行业通用标准进行对齐与映射。在人才盘点场景中，系统通过对员工简历、绩效记录、培训历史等多源数据的融合分析，自动生成每位员工的能力雷达图与胜任力评估报告，结合九宫格模型直观展示组织人才分布格局。基于盘点结果，系统可自动识别关键岗位的继任风险与发展储备，推荐内部潜力人才并进行个性化发展路径规划。</p>
        <p>在培训与发展领域，方案将能力缺口诊断与学习内容推荐深度结合。系统基于岗位能力标准与员工现状之间的差距，自动匹配平台课程库中的学习内容——涵盖在线课程、专家讲座、实操案例与实践项目等多种形式。培训管理者可以通过管理后台查看整体的技能差距热力图与学习者进度追踪，动态调整培训计划。方案同时支持与主流学习管理系统（LMS）的集成，实现培训数据的双向同步。在内部人才流动场景中，系统通过匹配员工的技能画像与内部岗位的能力要求，智能推荐空缺岗位的潜在人选候选列表，支持招聘经理进行快速筛选与定向推送。该方案已在金融服务、科技制造等多个行业头部客户中得到验证，平均将内部人才配置效率提升约40%。</p>

        <h4 class="section-chapter">二、招聘平台智能化升级方案</h4>
        <p>面向在线招聘平台与灵活用工平台，方案提供基于知识图谱与大模型的智能化升级能力。传统的招聘平台依赖标签匹配与关键词搜索，在人才与岗位的精准对接层面存在显著瓶颈——尤其对于技能要求复杂、跨界融合度高的岗位，现有匹配方式往往难以捕捉候选人的深层能力价值。本方案通过接入平台的岗位数据库与简历库，为其构建行业级的能力知识图谱，将平台上的所有岗位与人才信息统一到同一套能力语义体系下。所有的搜索与推荐流程均可在图谱层面运行，基于语义相似度与推理规则进行智能排序，而非简单的关键词命中。这一升级使得跨技能领域的隐性能力匹配成为可能——例如，具备游戏引擎开发能力的工程师可能被推荐至自动驾驶仿真系统岗位，因为两者共享计算机图形学与实时系统编程的核心能力基础。</p>
        <p>方案的另一大亮点是自动岗位标准化与质量增强模块。平台每天接收来自不同企业的海量岗位数据，缺乏统一的格式标准与质量保障。系统通过数据清洗与智能补全管道，自动识别岗位信息中的缺失字段、格式异常以及表述不规范问题，基于图谱中的同义关系与行业标准进行自动补全与纠偏。例如，当岗位描述中仅出现"熟练使用一种前端框架"时，系统可基于当前市场需求与行业数据，智能补全为对该岗位常见的具体技术栈建议。经过标准化处理后的岗位信息在搜索结果中可获得更高的曝光权重，同时也为求职者提供了更清晰、更一致的浏览体验。此外，方案还提供了岗位热度趋势分析、薪酬区间智能估算、招聘周期预测等增值模块，帮助运营团队进行数据驱动的决策优化。</p>

        <h4 class="section-chapter">三、教育与职业培训机构方案</h4>
        <p>面向职业教育机构、技术培训学院与高校就业指导中心，方案提供课程体系智能化设计与就业对接服务。教育培训机构普遍面临课程内容更新滞后于行业需求、培养方向与就业市场脱节等痛点。本方案通过持续监测企业招聘需求的变化趋势与技能需求的波动情况，为教育机构提供数据驱动的课程优化建议。系统能够将机构现有课程体系与能力图谱中的技能节点进行映射，识别出课程覆盖充分的知识领域与存在缺口的方向，并基于行业需求热度的变化趋势推荐需要新增或加强的教学内容。在课程设计层面，系统可根据目标岗位群体的能力要求，智能生成课程大纲草案与知识点串联路径，辅助课程设计团队进行快速迭代。</p>
        <p>在就业对接层面，方案构建了"学习—评估—推荐—反馈"的闭环机制。学员在校期间的学习成果——包括课程完成记录、项目实践成果、技能测验成绩等——均可整合为结构化的能力档案。毕业前，系统自动将该档案与平台上的活跃岗位进行匹配分析，生成个性化的就业推荐列表，并附带详细的匹配报告，帮助学员了解自身优势与待改进方向。对于培训机构的就业服务团队，系统提供批量化的学员能力分析看板，展示整体学员的能力分布、就业方向的集中程度以及与市场需求的匹配情况，支持就业指导老师进行有针对性的简历辅导与面试准备。方案已经在多家IT教育培训机构落地，学员就业匹配精度平均提升约35%，就业周期缩短约20%。</p>

        <h4 class="section-chapter">四、政府人才战略与公共服务方案</h4>
        <p>面向人社部门、人才服务局与产业园区管理机构，方案提供区域人才态势感知与产业人才规划辅助决策能力。传统的区域人才工作往往依赖抽样调查与经验判断，难以实现对人才供需全貌的精准掌握。本方案通过汇聚本地企业招聘数据、高校毕业生数据、人才流动数据以及产业经济数据等多源信息，构建区域级的人才态势感知系统。系统以可视化大屏与深度分析报告的形式，直观展示区域内的人才供给结构、企业岗位需求分布、紧缺技能清单、人才流入流出趋势以及薪资水平走势等关键指标。基于能力图谱的产业对标分析模块，可将区域内的人才结构与对标地区或全国平均水平进行横向比较，辅助识别区域人才竞争优势与潜在短板。</p>
        <p>在产业人才规划场景中，方案支持政府部门对重点产业——如人工智能、集成电路、生物医药等——进行专项人才供需预测与缺口分析。系统基于产业规划目标与能力图谱中对应岗位的技能要求，结合区域教育培养能力与外部人才供给潜力，构建多情景下的供需预测模型。预测结果可用于指导院校专业设置调整、人才引进政策制定、职业培训资源配置等决策。同时，方案为公共就业服务平台提供了智能化的岗位推荐与人才匹配能力，求职者与招聘方均可在统一平台上获得基于能力图谱的精准对接服务。方案还特别关注数据安全与隐私保护，所有数据采集与应用均遵循国家网络安全法与个人信息保护法的合规要求，确保公共服务的安全可靠运行。</p>
      </div>
    </el-dialog>

    <!-- ===== 文档中心弹窗 ===== -->
    <el-dialog :model-value="showSection === 'docs'" title="文档中心" width="780px" top="5vh" @close="showSection = ''" destroy-on-close>
      <div class="section-modal">
        <h4 class="section-chapter">一、快速入门指南</h4>
        <p>欢迎使用人才能力大脑平台。本指南将帮助您在最短时间内熟悉平台核心功能并完成首次操作。平台提供了三个用户角色入口：求职者、招聘者与管理员，每个角色拥有差异化的功能界面与操作权限。作为新用户，您首先需要通过注册页面创建一个账号。注册时请选择您的角色类型——求职者角色将进入用户端，可浏览岗位、上传简历并进行匹配分析；招聘者角色将进入HR端，可发布与管理岗位、查看求职者投递信息。注册完成后使用您的用户名与密码登录系统，即可进入对应角色的工作面板。登录后建议您先完善个人资料，包括基本信息与能力标签信息，这将有助于系统为您提供更精准的推荐服务。</p>
        <p>如果您是求职者，登录后建议首先体验"上传简历"功能。平台支持PDF、DOC、DOCX格式的简历文件，上传后系统将在数秒内完成自动解析并结构化展示您的个人信息与能力标签。接着可以前往"岗位发现"板块浏览平台上的活跃招聘信息，您可以通过搜索、筛选或分类导航等方式定位感兴趣的岗位。对于心仪的岗位，您可以在岗位详情页中启动"匹配分析"功能——系统将基于您的简历与岗位需求，生成详细的匹配报告，展示匹配得分、能力差距与改进建议。最后，"能力图谱"与"学习规划"板块将帮助您更清晰地了解自身技能定位与职业发展路线。</p>

        <h4 class="section-chapter">二、API 接口文档</h4>
        <p>本平台提供RESTful风格的API接口，支持第三方系统集成与数据对接。所有API端点均部署在 https://api.capability-brain.com/api/v1 下。接口采用Bearer Token认证方式，用户需先在平台注册并登录获取有效的访问令牌（Token），在请求头中以"Authorization: Bearer {token}"的形式携带。公共资源接口（如爬虫数据提交、智能体回调等）无需认证，但需要对请求来源IP进行白名单配置。API的请求体与响应体统一使用JSON格式编码，时间字段采用ISO 8601标准。所有接口的响应结构遵循统一规范——成功响应直接返回数据负载，错误响应包含code（错误码）、message（错误描述）与detail（详细错误信息）三个字段。</p>
        <p>核心业务接口分五大模块。用户认证模块包含注册POST /users/register、登录POST /users/login、获取当前用户信息GET /users/me以及修改密码POST /users/change-password。岗位数据模块包含岗位列表GET /jobs（支持分页、关键词搜索、状态与数据类型筛选）、岗位详情GET /jobs/{id}、岗位创建POST /jobs以及岗位信息更新PUT /jobs/{id}。简历管理模块提供简历上传POST /resumes/upload（支持multipart/form-data格式）、简历列表GET /resumes、简历解析结果获取GET /resumes/{id}以及简历文件下载GET /resumes/{id}/file（支持Token在URL参数中传递以实现新标签页直接打开）。匹配分析模块的核心接口为POST /match/run（触发人岗匹配分析）与GET /match/records（查询匹配记录列表）。管理后台模块则提供了管理员专用的数据统计、用户管理与系统配置接口。详细的接口参数说明与示例可在平台在线Swagger文档中查看。</p>

        <h4 class="section-chapter">三、数据安全与隐私说明</h4>
        <p>平台高度重视用户数据的安全与隐私保护。所有数据传输过程均采用TLS 1.3加密协议，确保客户端与服务器之间的通信安全。存储层面，用户的敏感信息——包括密码、联系方式、身份信息等——均经过加密处理后保存。密码采用PBKDF2加盐哈希算法进行单向加密，即使数据库发生泄露也无法逆向还原原始密码。简历文件存储在隔离的文件存储系统中，仅通过带Token验证的临时授权链接方可访问，且链接具有时效性限制，过期后自动失效。平台严格遵守《中华人民共和国个人信息保护法》与《中华人民共和国数据安全法》的相关规定，不会在未获得用户明确授权的情况下将用户数据用于系统功能之外的任何场景。</p>
        <p>平台在架构设计层面实施了最小权限原则与数据隔离策略。不同角色的用户仅能访问与其权限匹配的功能模块与数据范围。普通用户仅可查看与操作自己的简历数据与匹配记录，招聘者仅可管理自己发布的岗位以及对应岗位的求职者投递信息，管理员拥有系统级的管理权限但所有操作均被记录在审计日志中。系统对每一次数据访问与操作均生成不可篡改的审计记录，涵盖操作时间、操作用户、操作类型、目标对象以及操作结果等信息，确保任何数据变更都有据可查。平台定期进行安全漏洞扫描与渗透测试，并与第三方安全机构合作进行独立审计，确保系统的整体安全防护能力达到行业领先水平。</p>

        <h4 class="section-chapter">四、最佳实践与操作技巧</h4>
        <p>为了获得最佳的使用体验与最准确的分析结果，建议您遵循以下实践指南。首先，关于简历上传的优化：请确保上传的简历为最新版本，且文件格式为PDF或DOCX这两种主流格式，避免使用图片式PDF或扫描件格式（此类文件会增加解析的难度与不准确性）。简历内容中请尽量使用标准化的技能表述方式——例如"Java""Python""Spring Boot""React"等通用技术名词，而非模糊的描述如"精通多种编程语言""熟悉常用框架"等。明确的技能表述将显著提升系统对您能力标签的识别准确率与匹配结果的参考价值。如果简历中包含GitHub链接、个人博客或作品集地址，建议一并填入，这些信息将作为能力评估的辅助参考。</p>
        <p>其次，关于匹配分析的使用建议。在启动匹配分析前，请确认已选择您感兴趣的岗位与您本人的简历作为分析对象。匹配分析通常需要数十秒的运算时间，系统的AI模型会从多个维度对您与目标岗位进行评估。在查看报告时，请重点关注"差距分析"板块中的高优先级项目——这些是匹配得分影响最大的关键能力项。对于差距分析中识别出的技能缺口，可以结合"学习规划"模块制定针对性的提升计划，平台会根据您现有的能力基础与目标岗位要求，推荐最适合的学习资源与进阶路径。最后，建议您定期更新简历与能力信息，并持续关注"岗位发现"中的最新招聘动态——平台的能力图谱每日更新，岗位数据实时刷新，保持活跃的使用频次将有助于您第一时间获取最有价值的职业信息。</p>
      </div>
    </el-dialog>

    <!-- ===== 关于我们弹窗 ===== -->
    <el-dialog :model-value="showSection === 'about'" title="关于我们" width="780px" top="5vh" @close="showSection = ''" destroy-on-close>
      <div class="section-modal">
        <h4 class="section-chapter">公司介绍</h4>
        <p>人才能力大脑科技有限公司成立于2023年，是一家专注于人工智能与知识工程技术在人才与组织发展领域应用的创新型科技企业。公司总部位于北京中关村科技园区，在上海、深圳、杭州设有研发中心与业务办事处。公司的创始团队来自北大、清华、中科院等顶尖高校与科研机构，核心成员在自然语言处理、知识图谱构建、智能推荐系统以及人力资源科技领域拥有十余年的研发与实践经验。自成立以来，公司始终坚持以"让每一份能力都被看见"为使命，致力于通过先进的人工智能技术重构人才识别、评估与发展的全链条流程，推动中国人才管理领域的数字化转型与智能化升级。</p>
        <p>公司的核心产品——人才能力大脑（Capability Brain）——一经推出便获得了业界与市场的广泛认可。平台在2024年先后荣获"中国人工智能创新创业大赛「最佳技术创新奖」"与"HRTech中国「年度最佳人才科技产品」"两项行业大奖，并被多家头部投资机构列为重点关注项目。截至目前，平台累计服务企业客户超过200家，覆盖金融、科技、制造、医疗、教育等多个核心行业领域，注册个人用户突破5万人。公司与腾讯云、阿里云、百度AI等头部技术平台建立了深度合作伙伴关系，在算力资源、大模型能力与行业数据等方面获得了全方位的技术支撑。我们正以每年超过200%的数据增长速度，持续扩充与更新能力图谱的覆盖范围与深度，力争在三年内建成国内最大、最权威的人才能力知识网络。</p>

        <h4 class="section-chapter">技术实力</h4>
        <p>公司在核心技术能力方面建立了系统的技术栈与研发体系。底层基础设施层，平台采用基于Kubernetes的微服务架构，实现了各业务模块的独立部署、弹性伸缩与容灾恢复。存储层使用MySQL作为关系型数据库存储核心业务数据，结合Elasticsearch构建全文搜索能力，引入Neo4j图数据库承载能力图谱的语义关系网络，形成"关系型+文档型+图型"三合一的混合存储架构。AI模型层，平台自研了面向人才领域的预训练语言模型——CapBERT，该模型在百万级专业语料上进行了领域预训练与任务微调，在简历解析、人岗匹配、技能识别等核心任务上表现优异。知识图谱构建层，平台自主研发了一套从多源异构数据到结构化知识的全自动流水线，集成实体识别、关系抽取、实体链接、知识融合等NLP核心组件，每小时可处理超过10万条原始数据的知识化转换。</p>
        <p>平台的工程化能力同样经受了大规模场景的检验。后端核心服务使用Python FastAPI框架开发，前端采用Vue 3 + TypeScript技术栈，配合Element Plus组件库构建了统一且高效的用户界面。在并发处理方面，系统设计了基于Redis的消息队列用于异步任务调度——简历解析、匹配分析、数据爬取等耗时操作均通过任务队列异步执行，前端通过轮询机制获取处理进度与结果。对于匹配分析这一计算密集型任务，系统采用GPU加速推理，单次匹配分析的响应时间控制在10秒以内。在数据安全方面，平台通过了国家信息系统安全等级保护二级认证，并建立了完整的数据备份与灾难恢复机制，RPO（恢复点目标）不超过15分钟，RTO（恢复时间目标）不超过2小时。目前平台核心系统可用性维持在99.9%以上，能够为大规模企业用户与个人用户提供稳定可靠的服务体验。</p>

        <h4 class="section-chapter">企业文化</h4>
        <p>公司的企业文化根植于"专业、创新、务实、共赢"的核心价值观。在专业层面，我们坚持技术深耕与行业理解并重，要求每一位团队成员既具备过硬的技术功底，又深刻理解人才管理业务的本质逻辑。团队内部设立了常态化的技术分享与业务研讨机制，每周开展前沿论文研读、技术方案评审与行业趋势分析等活动，确保团队的知识储备与技术视野始终保持行业领先。在创新层面，我们鼓励自下而上的技术探索与产品创新，设立了"创新实验室"机制——每个季度团队成员可以提出创新项目提案，通过评审后可以获得专属的开发资源与时间进行原型验证。这些创新项目中的优秀成果会定期被吸纳进入核心产品，形成了从研究探索到工程落地的正向循环。</p>
        <p>务实与共赢是公司的行为准则与商业信条。我们坚信，技术产品的最终价值体现在为客户创造的实际效益之中。在每一个项目实施过程中，我们的团队都会深入客户业务一线，与客户的HR团队、IT团队以及业务管理者进行多渠道沟通，确保产品方案真正贴合实际需求而非纸上谈兵。我们设立了客户成功团队，建立了常态化的客户反馈收集与产品迭代机制，每两周发布一个迭代版本，每月进行一次重大功能更新。在商业伙伴关系层面，我们坚持开放合作的生态策略，与行业内的咨询公司、培训机构、技术平台以及研究机构建立了广泛的合作关系，共同推动人才能力管理领域的知识共享与技术进步。我们期待与更多的合作伙伴和客户一起，共同建设一个更加公平、高效、智能的人才能力匹配新生态。</p>
      </div>
    </el-dialog>

    <!-- 特色功能 -->
    <section class="feature-cards">
      <div class="feature-card">
        <div class="feature-icon">FIND</div>
        <h3 class="feature-title">新岗位发现</h3>
        <p class="feature-desc">基于多源数据智能识别新兴岗位，自动生成标准化岗位定义，支持人工优化与动态更新。</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">GRAPH</div>
        <h3 class="feature-title">能力图谱</h3>
        <p class="feature-desc">构建技能级能力图谱，展示领域内岗位能力要求，支持按技术栈和级别切换视图。</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">MATCH</div>
        <h3 class="feature-title">精准匹配</h3>
        <p class="feature-desc">多维度人岗匹配分析，智能差距诊断，提供针对性改进建议与学习路径规划。</p>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-links">
        <a href="javascript:void(0)" class="footer-link">服务条款</a>
        <a href="javascript:void(0)" class="footer-link">隐私政策</a>
        <a href="javascript:void(0)" class="footer-link">安全保障</a>
        <a href="javascript:void(0)" class="footer-link">联系我们</a>
      </div>
      <div class="footer-copyright">
        &copy; 2024 人才能力大脑. All rights reserved.
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const errorMsg = ref('')
const rememberMe = ref(true)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

// 注册
const registerDialogVisible = ref(false)
const registerLoading = ref(false)
const registerFormRef = ref<FormInstance>()

const showSection = ref('')
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  role: 'user'
})
const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少3位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次密码输入不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

async function handleRegister() {
  const valid = await registerFormRef.value?.validate().catch(() => false)
  if (!valid) return

  registerLoading.value = true
  try {
    await api.post('/users/register', {
      username: registerForm.username,
      password: registerForm.password,
      role: registerForm.role
    })
    ElMessage.success('注册成功，请登录')
    registerDialogVisible.value = false
    loginForm.username = registerForm.username
    registerForm.username = ''
    registerForm.password = ''
    registerForm.confirmPassword = ''
    registerForm.role = 'user'
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.detail || '注册失败')
  } finally {
    registerLoading.value = false
  }
}

// ===== 管理员隐藏入口 =====
const adminDialogVisible = ref(false)
const adminLoading = ref(false)
const adminError = ref('')
const adminFormRef = ref<FormInstance>()
const adminForm = reactive({
  username: '',
  password: ''
})
const adminRules: FormRules = {
  username: [{ required: true, message: '请输入管理员账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入管理员密码', trigger: 'blur' }]
}

async function handleAdminLogin() {
  const valid = await adminFormRef.value?.validate().catch(() => false)
  if (!valid) return

  adminLoading.value = true
  adminError.value = ''
  try {
    const res: any = await api.post('/admin/login', {
      username: adminForm.username,
      password: adminForm.password
    })
    const token = res.access_token
    userStore.setUser({
      id: 0,
      username: 'admin',
      role: 'admin',
      token: token
    })
    adminDialogVisible.value = false
    router.push('/admin')
  } catch (err: any) {
    adminError.value = err.response?.data?.detail || '验证失败，请重试'
    adminForm.password = ''
  } finally {
    adminLoading.value = false
  }
}

onMounted(() => {
  if (window.location.pathname === '/login/admin') {
    adminDialogVisible.value = true
  }
})

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  errorMsg.value = ''

  try {
    await userStore.login(loginForm.username, loginForm.password)
    if (userStore.isAdmin) {
      router.push('/admin')
    } else if (userStore.user?.role === 'hr') {
      router.push('/hr')
    } else {
      router.push('/user')
    }
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '用户名或密码错误，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #ffffff;
  color: #1e293b;
  overflow-x: hidden;
  position: relative;
}

/* ===== 背景装饰 ===== */
.bg-pattern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.network-grid {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    linear-gradient(rgba(59, 130, 246, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

/* ===== 顶部导航 ===== */
.header {
  position: relative;
  z-index: 10;
  padding: 24px 48px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #0f172a;
}

.logo-dot {
  color: #3b82f6;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: #64748b;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #0f172a;
}

/* ===== 主内容区 ===== */
.main-content {
  position: relative;
  z-index: 10;
  display: flex;
  min-height: calc(100vh - 80px - 200px);
}

/* -- Hero -- */
.hero-section {
  flex: 1;
  padding: 80px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 20px;
  line-height: 1.2;
  color: #0f172a;
}

.hero-highlight {
  background: linear-gradient(90deg, #3b82f6, #0ea5e9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 16px;
  color: #64748b;
  line-height: 1.8;
  max-width: 600px;
  margin-bottom: 40px;
}

.hero-stats {
  display: flex;
  gap: 48px;
}

.hero-stat {
  text-align: center;
}

.hero-stat-value {
  font-size: 36px;
  font-weight: 700;
  color: #3b82f6;
}

.hero-stat-label {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 4px;
}

/* -- 登录 -- */
.login-section {
  width: 420px;
  padding: 80px 40px;
  background: rgba(0, 0, 0, 0.02);
  border-left: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-card {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  padding: 40px 32px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #0f172a;
}

.login-subtitle {
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 32px;
}

.login-form {
  width: 100%;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.forgot-link {
  font-size: 13px;
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.3s;
}

.forgot-link:hover {
  color: #0ea5e9;
}

.login-btn {
  width: 100%;
  height: 48px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
  border: none;
}

.login-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #0284c7 100%);
}

.signup-link {
  text-align: center;
  margin-top: 24px;
  font-size: 13px;
  color: #94a3b8;
}

.signup-link a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.signup-link a:hover {
  text-decoration: underline;
}

.role-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.role-selector .el-radio {
  width: 100%;
  height: auto;
  margin-right: 0;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 16px;
  transition: all 0.2s;
}

.role-selector .el-radio.is-checked {
  border-color: #3b82f6;
  background: #f8faff;
}

.role-option {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.role-label {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.role-desc {
  font-size: 12px;
  color: #94a3b8;
}

.error-message {
  display: none;
  padding: 12px;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 6px;
  font-size: 13px;
  color: #dc2626;
  margin-bottom: 16px;
}

.error-message.show {
  display: block;
}

.admin-error {
  padding: 8px 12px;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 6px;
  font-size: 13px;
  color: #dc2626;
  margin: 0;
}

/* 覆盖 Element Plus 输入框样式 */
:deep(.custom-input .el-input__wrapper) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: none !important;
  padding-left: 12px;
}

:deep(.custom-input .el-input__wrapper:hover) {
  border-color: #3b82f6;
}

:deep(.custom-input .el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

:deep(.custom-input .el-input__inner) {
  height: 48px;
  font-size: 14px;
}

:deep(.custom-input .el-input__prefix) {
  margin-right: 8px;
}

:deep(.custom-input .el-input__prefix-inner .el-icon) {
  font-size: 18px;
  color: #94a3b8;
}

/* ===== 特色功能 ===== */
.feature-cards {
  position: relative;
  z-index: 10;
  padding: 48px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  background: rgba(0, 0, 0, 0.02);
}

.feature-card {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  padding: 28px;
  transition: all 0.3s;
}

.feature-card:hover {
  border-color: rgba(59, 130, 246, 0.3);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.08);
}

.feature-icon {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #3b82f6;
  padding: 8px 12px;
  background: rgba(59, 130, 246, 0.08);
  border-radius: 4px;
  margin-bottom: 16px;
  display: inline-block;
}

.feature-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #0f172a;
}

.feature-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
}

/* ===== 页脚 ===== */
.footer {
  position: relative;
  z-index: 10;
  padding: 32px 48px;
  background: rgba(0, 0, 0, 0.02);
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-link {
  font-size: 12px;
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-link:hover {
  color: #64748b;
}

.footer-copyright {
  font-size: 12px;
  color: #cbd5e1;
}

/* ===== 响应式 ===== */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 36px;
  }

  .login-section {
    width: 360px;
    padding: 60px 30px;
  }

  .feature-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .header {
    padding: 16px 24px;
  }

  .nav-links {
    display: none;
  }

  .main-content {
    flex-direction: column;
  }

  .hero-section {
    padding: 40px 24px;
  }

  .hero-title {
    font-size: 28px;
  }

  .hero-stats {
    gap: 24px;
  }

  .hero-stat-value {
    font-size: 28px;
  }

  .login-section {
    width: 100%;
    padding: 40px 24px;
    border-left: none;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
  }

  .feature-cards {
    grid-template-columns: 1fr;
    padding: 24px;
  }

  .footer {
    flex-direction: column;
    gap: 16px;
    padding: 24px;
  }
}
</style>

<!-- ===== 弹窗内容全局样式（Dialog 渲染在 body 外，scoped 不生效） ===== -->
<style>
.section-modal {
  max-height: 68vh;
  overflow-y: auto;
  padding: 0 4px;
}

.section-modal::-webkit-scrollbar { width: 6px; }
.section-modal::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 3px; }
.section-modal::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }

.section-chapter {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 24px 0 12px;
  padding: 10px 14px;
  background: #f8fafc;
  border-left: 3px solid #3b82f6;
  border-radius: 4px;
}

.section-chapter:first-child { margin-top: 0; }

.section-modal p {
  font-size: 14px;
  color: #475569;
  line-height: 2;
  margin: 0 0 16px;
  text-indent: 2em;
  text-align: justify;
  padding: 0 6px;
}

/* Dialog 内边距优化 */
.el-dialog--default {
  --el-dialog-content-font-size: 14px;
}

.el-dialog__body {
  padding: 20px 24px !important;
}

.el-dialog__header {
  padding: 18px 24px 14px !important;
  margin-right: 0 !important;
  border-bottom: 1px solid #e2e8f0;
}

.el-dialog__title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
}
</style>
