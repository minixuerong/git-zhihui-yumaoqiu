<template>
  <div class="graph-panel">
    <div class="header">
      <div>
        <h1>能力图谱</h1>
        <p>可视化展示岗位与技能之间的关联关系</p>
      </div>
      <div class="category-filter">
        <el-select v-model="selectedCategory" placeholder="选择分类" @change="onCategoryChange">
          <el-option label="全部" value="all" />
          <el-option v-for="cat in categories" :key="cat.name" :label="cat.name" :value="cat.name" />
        </el-select>
      </div>
    </div>

    <div class="main-content">
      <div class="graph-container" ref="chartRef"></div>
      <div class="detail-panel" v-if="selectedNode">
        <div class="detail-header">
          <h3>{{ selectedNode.name }}</h3>
          <span class="detail-type" :class="selectedNode.category === 8 ? 'skill' : 'job'">
            {{ selectedNode.category === 8 ? '技能' : '岗位' }}
          </span>
        </div>
        <div class="detail-info">
          <div class="info-item">
            <span class="label">分类</span>
            <span class="value">{{ selectedNode.categoryName || '技能' }}</span>
          </div>
          <div class="info-item" v-if="selectedNode.value">
            <span class="label">关联数量</span>
            <span class="value">{{ selectedNode.value }}</span>
          </div>
          <div class="info-item" v-if="selectedNode.isEmerging">
            <span class="label">状态</span>
            <span class="value emerging">新兴技能</span>
          </div>
        </div>
        <div class="related-section" v-if="relatedSkills.length">
          <h4>关联技能</h4>
          <div class="skill-tags">
            <span v-for="skill in relatedSkills" :key="skill.skill" class="skill-tag" :class="{ emerging: skill.isEmerging }">
              {{ skill.skill }}
              <span class="tag-badge">{{ skill.frequency }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="legend-bar">
      <div class="legend-item" v-for="(color, index) in categoryColors" :key="index">
        <span class="legend-dot" :style="{ backgroundColor: color }"></span>
        <span class="legend-text">{{ categoryNames[index] }}</span>
      </div>
      <div class="legend-tips">
        <span>🖱️ 滚动缩放</span>
        <span>🖱️ 拖拽平移</span>
        <span>👆 点击查看详情</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import graphData from '@/assets/graph_data.json'

interface Node {
  id: string
  name: string
  category: number
  categoryName?: string
  symbolSize: number
  value: number
  isEmerging?: boolean
}

interface SkillInfo {
  skill: string
  frequency: number
  avgConfidence: number
  isEmerging: boolean
}

const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: echarts.ECharts | null = null
let observer: MutationObserver | null = null

const categories = computed(() => graphData.categories)

const categoryNames = computed(() => graphData.categories.map(c => c.name))

const categoryColors = [
  '#5470c6',
  '#91cc75',
  '#fac858',
  '#ee6666',
  '#73c0de',
  '#3ba272',
  '#fc8452',
  '#9a60b4',
  '#ea7ccc'
]

const selectedCategory = ref('all')
const selectedNode = ref<Node | null>(null)
const relatedSkills = computed<SkillInfo[]>(() => {
  if (!selectedNode.value || selectedNode.value.category === 8) return []
  return (graphData.jobSkills as Record<string, SkillInfo[]>)[selectedNode.value.name] || []
})

const filteredData = computed(() => {
  if (selectedCategory.value === 'all') {
    return {
      nodes: graphData.nodes,
      links: graphData.links
    }
  }
  const catIndex = graphData.categories.findIndex(c => c.name === selectedCategory.value)
  const filteredNodes = graphData.nodes.filter(node => {
    if (catIndex === 8) {
      return node.category === 8
    }
    return node.category === catIndex || node.category === 8
  })
  const nodeIds = new Set(filteredNodes.map(n => n.id))
  const filteredLinks = graphData.links.filter(link => 
    nodeIds.has(link.source as string) && nodeIds.has(link.target as string)
  )
  return { nodes: filteredNodes, links: filteredLinks }
})

function initChart() {
  if (!chartRef.value) return
  
  const container = chartRef.value
  if (!container.clientWidth || !container.clientHeight) {
    return
  }
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(container)
  
  const option: echarts.EChartsOption = {
    backgroundColor: {
      type: 'linear',
      x: 0,
      y: 0,
      x2: 1,
      y2: 1,
      colorStops: [
        { offset: 0, color: '#e8f4fc' },
        { offset: 1, color: '#f0f7ff' }
      ]
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          const node = params.data as Node
          const type = node.category === 8 ? '技能' : '岗位'
          const emerging = node.isEmerging ? '<br/>📈 新兴技能' : ''
          return `<strong>${node.name}</strong><br/>类型: ${type}<br/>关联数: ${node.value}${emerging}`
        } else {
          return `${params.data.source} → ${params.data.target}<br/>权重: ${params.data.value}`
        }
      }
    },
    legend: {
      show: false
    },
    series: [
      {
        name: '能力图谱',
        type: 'graph',
        layout: 'force',
        data: filteredData.value.nodes.map((node: Node) => ({
          ...node,
          itemStyle: {
            color: node.category === 8 ? '#9a60b4' : categoryColors[node.category],
            borderColor: '#fff',
            borderWidth: 2,
            shadowBlur: 10,
            shadowColor: 'rgba(0,0,0,0.15)'
          },
          label: {
            show: true,
            position: node.category === 8 ? 'bottom' : 'top',
            fontSize: node.category === 8 ? 12 : 14,
            fontWeight: node.category === 8 ? 'normal' : 'bold',
            color: node.category === 8 ? '#555' : '#333',
            distance: 8,
            formatter: (params: any) => params.name,
            alignTo: 'edge',
            edgeDistance: 20
          },
          emphasis: {
            scale: true,
            itemStyle: {
              shadowBlur: 20,
              shadowColor: 'rgba(0,0,0,0.3)'
            },
            label: {
              fontSize: node.category === 8 ? 14 : 16
            }
          },
          mass: node.category === 8 ? 2 : 8
        })),
        links: filteredData.value.links.map(link => ({
          ...link,
          lineStyle: {
            width: link.lineStyle?.width || 1,
            opacity: link.lineStyle?.opacity || 0.6,
            color: '#ccc'
          }
        })),
        categories: graphData.categories.map((cat, index) => ({
          name: cat.name,
          itemStyle: {
            color: categoryColors[index]
          }
        })),
        roam: true,
        draggable: true,
        force: {
          repulsion: 1200,
          gravity: 0.02,
          edgeLength: [250, 500],
          layoutAnimation: true,
          friction: 0.5,
          nodeDistance: 300
        },
        select: {
          itemStyle: {
            borderColor: '#ff6b6b',
            borderWidth: 3
          }
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        },
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut'
      }
    ]
  }
  
  chartInstance.setOption(option)
  
  chartInstance.on('click', (params: any) => {
    if (params.dataType === 'node') {
      selectedNode.value = params.data
    } else {
      selectedNode.value = null
    }
  })
}

function onCategoryChange() {
  nextTick(() => {
    initChart()
  })
}

function handleResize() {
  nextTick(() => {
    if (chartInstance) {
      chartInstance.resize()
    } else {
      initChart()
    }
  })
}

let visibilityTimer: number | null = null

function checkVisibility() {
  if (!chartRef.value || chartInstance) return
  const container = chartRef.value
  if (container.clientWidth && container.clientHeight) {
    initChart()
    if (visibilityTimer) {
      clearInterval(visibilityTimer)
      visibilityTimer = null
    }
  }
}

onMounted(() => {
  nextTick(() => {
    checkVisibility()
  })
  
  window.addEventListener('resize', handleResize)
  
  observer = new MutationObserver(() => {
    nextTick(checkVisibility)
  })
  
  if (chartRef.value && chartRef.value.parentElement) {
    observer.observe(chartRef.value.parentElement, {
      attributes: true,
      childList: true,
      subtree: true
    })
  }
  
  visibilityTimer = window.setInterval(() => {
    checkVisibility()
  }, 300)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  observer?.disconnect()
  if (visibilityTimer) {
    clearInterval(visibilityTimer)
    visibilityTimer = null
  }
  chartInstance?.dispose()
})

watch(filteredData, () => {
  nextTick(() => {
    initChart()
  })
})
</script>

<style scoped>
.graph-panel {
  padding: 0;
  height: calc(100vh - 80px);
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.header p {
  font-size: 14px;
  color: #999;
  margin: 4px 0 0;
}

.category-filter {
  width: 200px;
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.graph-container {
  flex: 1;
  height: 100%;
  min-height: 400px;
}

.detail-panel {
  width: 320px;
  background: #fff;
  border-left: 1px solid #e8e8e8;
  padding: 20px;
  overflow-y: auto;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.detail-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.detail-type {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.detail-type.job {
  background: #e6f7ff;
  color: #1890ff;
}

.detail-type.skill {
  background: #f9f0ff;
  color: #722ed1;
}

.detail-info {
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item .label {
  font-size: 13px;
  color: #999;
}

.info-item .value {
  font-size: 13px;
  color: #333;
  font-weight: 500;
}

.info-item .value.emerging {
  color: #faad14;
}

.related-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #f5f5f5;
  border-radius: 20px;
  font-size: 12px;
  color: #666;
}

.skill-tag.emerging {
  background: #fffbe6;
  color: #d48806;
}

.tag-badge {
  background: #1890ff;
  color: #fff;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 10px;
}

.skill-tag.emerging .tag-badge {
  background: #faad14;
}

.legend-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #fff;
  border-top: 1px solid #e8e8e8;
  flex-wrap: wrap;
  gap: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-right: 16px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-text {
  font-size: 12px;
  color: #666;
}

.legend-tips {
  display: flex;
  gap: 16px;
}

.legend-tips span {
  font-size: 12px;
  color: #999;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .detail-panel {
    width: 100%;
    border-left: none;
    border-top: 1px solid #e8e8e8;
    height: 200px;
  }
  
  .legend-bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>