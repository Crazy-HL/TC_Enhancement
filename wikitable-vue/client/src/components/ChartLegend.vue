<template>
	<div class="chart-legend-container">
		<!-- 饼图图注 -->
		<div class="pie-legend">
			<div class="pie-chart" :style="pieChartStyle"></div>
			<div class="legend-labels horizontal">
				<div v-for="item in typeLegend" :key="item.label" class="legend-label">
					<span
						class="legend-color"
						:style="{ backgroundColor: item.color }"></span>
					<span class="legend-text">{{ item.label }}</span>
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
</script>

<style scoped>
	.chart-legend-container {
		display: flex;
		gap: 15px;
	}

	.pie-legend {
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

	.legend-labels {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.legend-labels.horizontal {
		flex-direction: row;
		flex-wrap: wrap;
		align-items: center;
	}

	.legend-label {
		display: flex;
		align-items: center;
		gap: 4px;
		font-size: 12px;
		line-height: 1.2;
		margin-right: 8px;
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
		.pie-legend {
			flex-direction: column;
			align-items: flex-start;
		}

		.legend-labels.horizontal {
			flex-direction: row;
			flex-wrap: wrap;
			gap: 8px;
		}
	}
</style>
