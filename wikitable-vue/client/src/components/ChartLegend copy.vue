<template>
	<div class="chart-legend-container">
		<!-- 饼图图注 -->
		<div class="chart-group" v-if="showPieChart">
			<div class="pie-legend">
				<div class="pie-chart" :style="pieChartStyle"></div>
				<div class="legend-labels">
					<div
						v-for="item in typeLegend"
						:key="item.label"
						class="legend-label">
						<span
							class="legend-color"
							:style="{ backgroundColor: item.color }"></span>
						<span class="legend-text">{{ item.label }}</span>
					</div>
				</div>
			</div>
		</div>

		<!-- 堆叠图图注 - 固定比例显示 -->
		<div class="chart-group" v-if="showStackedChart">
			<div class="stacked-legend">
				<div class="stacked-chart">
					<div class="bar-segment support"></div>
					<div class="bar-segment neutral"></div>
					<div class="bar-segment oppose"></div>
				</div>
				<div class="legend-labels">
					<div
						v-for="item in standpointLegend"
						:key="item.label"
						class="legend-label">
						<span
							class="legend-color"
							:style="{ backgroundColor: item.color }"></span>
						<span class="legend-text">{{ item.label }}</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { computed } from "vue";

	const props = defineProps({
		comments: {
			type: Array,
			required: true
		},
		showPieChart: {
			type: Boolean,
			default: true
		},
		showStackedChart: {
			type: Boolean,
			default: true
		}
	});

	// 类型数据计算
	const typeStats = computed(() => {
		const stats = {
			statement: 0,
			question: 0,
			exclamation: 0,
			suggestion: 0,
			sarcasm: 0,
			total: 0
		};

		props.comments.forEach(comment => {
			const type = comment.comment_type || 1;
			if (type === 1) stats.statement++;
			else if (type === 2) stats.question++;
			else if (type === 3) stats.exclamation++;
			else if (type === 4) stats.suggestion++;
			else if (type === 5) stats.sarcasm++;
			stats.total++;
		});

		return {
			statement: stats.statement,
			question: stats.question,
			exclamation: stats.exclamation,
			suggestion: stats.suggestion,
			sarcasm: stats.sarcasm,
			total: stats.total
		};
	});

	// 饼图样式
	const pieChartStyle = computed(() => {
		const { statement, question, exclamation, suggestion, sarcasm, total } =
			typeStats.value;
		if (total === 0) return { background: "#f0f0f0" };

		const statementPct = (statement / total) * 100;
		const questionPct = (question / total) * 100;
		const exclamationPct = (exclamation / total) * 100;
		const suggestionPct = (suggestion / total) * 100;
		const sarcasmPct = (sarcasm / total) * 100;

		return {
			background: `conic-gradient(
      #4285f4 0% ${statementPct}%,
      #ea4335 ${statementPct}% ${statementPct + questionPct}%,
      #34a853 ${statementPct + questionPct}% ${
				statementPct + questionPct + exclamationPct
			}%,
      #9c27b0 ${statementPct + questionPct + exclamationPct}% ${
				statementPct + questionPct + exclamationPct + suggestionPct
			}%,
      #ff9800 ${
				statementPct + questionPct + exclamationPct + suggestionPct
			}% 100%
    )`,
			width: "40px",
			height: "40px",
			borderRadius: "50%"
		};
	});

	// 类型图注
	const typeLegend = [
		{ label: "陈述", key: "statement", color: "#4285f4" },
		{ label: "疑问", key: "question", color: "#ea4335" },
		{ label: "感叹", key: "exclamation", color: "#34a853" },
		{ label: "建议", key: "suggestion", color: "#9c27b0" },
		{ label: "讽刺", key: "sarcasm", color: "#ff9800" }
	];

	// 立场图注
	const standpointLegend = [
		{ label: "支持", key: "support", color: "#ccebc5" },
		{ label: "反对", key: "oppose", color: "#fbb4ae" },
		{ label: "中立", key: "neutral", color: "#b3cde3" }
	];
</script>

<style scoped>
	.chart-legend-container {
		display: flex;
		gap: 15px;
	}

	.chart-group {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.pie-legend,
	.stacked-legend {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.pie-chart {
		width: 40px;
		height: 40px;
		border-radius: 50%;
		flex-shrink: 0;
		background: #f0f0f0; /* 默认背景色 */
	}

	.stacked-chart {
		width: 20px;
		height: 40px;
		display: flex;
		flex-direction: column;
		background: #f5f5f5;
		border-radius: 3px;
		overflow: hidden;
	}

	.stacked-bar {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
	}

	.bar-segment {
		width: 100%;
		flex-grow: 1; /* 每个部分平均分配高度 */
	}

	.bar-segment.support {
		background-color: #ccebc5;
	}

	.bar-segment.neutral {
		background-color: #b3cde3;
	}

	.bar-segment.oppose {
		background-color: #fbb4ae;
	}

	.legend-labels {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.legend-label {
		display: flex;
		align-items: center;
		gap: 4px;
		font-size: 12px;
		line-height: 1.2;
	}

	.legend-color {
		width: 10px;
		height: 10px;
		border-radius: 2px;
		flex-shrink: 0;
		display: inline-block;
	}

	.legend-text {
		white-space: nowrap;
		color: #555;
	}

	@media (max-width: 768px) {
		.chart-legend-container {
			flex-direction: column;
			gap: 8px;
		}

		.pie-legend,
		.stacked-legend {
			flex-direction: column;
			align-items: flex-start;
		}

		.legend-labels {
			flex-direction: row;
			flex-wrap: wrap;
			gap: 8px;
		}
	}
</style>
