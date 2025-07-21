<template>
	<span class="comment-stats">
		<!-- 立场堆叠图 -->
		<span
			v-if="showStandpoint"
			class="standpoint-chart"
			:title="standpointTooltip"
			:style="standpointStyle">
			<span class="stacked-bar">
				<span class="bar-segment support"></span>
				<span class="bar-segment neutral"></span>
				<span class="bar-segment oppose"></span>
			</span>
		</span>

		<!-- 类型饼图 -->
		<span
			v-if="showType"
			class="type-pie-chart"
			:title="typeTooltip"
			:style="{
				...pieChartStyle,
				width: pieChartSize + 'px',
				height: pieChartSize + 'px'
			}"></span>
	</span>
</template>

<script setup>
	import { computed } from "vue";

	const props = defineProps({
		comments: {
			type: Array,
			required: true
		},
		showStandpoint: {
			type: Boolean,
			default: true
		},
		showType: {
			type: Boolean,
			default: false
		},
		showEmotion: {
			type: Boolean,
			default: true
		}
	});

	// 计算饼图大小 - 基于评论数量动态调整 (8px-16px)
	const pieChartSize = computed(() => {
		const count = props.comments.length;
		if (count <= 1) return 8; // 最小尺寸
		if (count >= 10) return 20; // 最大尺寸不超过行高
		return 8 + Math.round((count / 10) * 8); // 线性增长
	});

	// 类型相关方法
	const getCommentType = comment => {
		return comment?.comment_type || 1;
	};

	const getCommentTypeLabel = comment => {
		const type = getCommentType(comment);
		const types = {
			1: "陈述",
			2: "疑问",
			3: "感叹",
			4: "建议",
			5: "讽刺"
		};
		return types[type] || "陈述";
	};

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
			const type = getCommentType(comment);
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

	// 类型tooltip
	const typeTooltip = computed(() => {
		const { statement, question, exclamation, suggestion, sarcasm, total } =
			typeStats.value;
		if (total === 0) return "无类型数据";

		const statementPct = Math.round((statement / total) * 100);
		const questionPct = Math.round((question / total) * 100);
		const exclamationPct = Math.round((exclamation / total) * 100);
		const suggestionPct = Math.round((suggestion / total) * 100);
		const sarcasmPct = Math.round((sarcasm / total) * 100);

		return `陈述: ${statement} (${statementPct}%)
疑问: ${question} (${questionPct}%)
感叹: ${exclamation} (${exclamationPct}%)
建议: ${suggestion} (${suggestionPct}%)
讽刺: ${sarcasm} (${sarcasmPct}%)`;
	});

	// 饼图样式
	const pieChartStyle = computed(() => {
		const { statement, question, exclamation, suggestion, sarcasm, total } =
			typeStats.value;
		if (total === 0) return {};

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
      )`
		};
	});

	// 立场数据计算
	const standpointStats = computed(() => {
		const stats = { support: 0, oppose: 0, neutral: 0, total: 0 };

		props.comments.forEach(comment => {
			if (comment.standpoint === 1) stats.support++;
			else if (comment.standpoint === -1) stats.oppose++;
			else stats.neutral++;
			stats.total++;
		});

		return stats;
	});

	// 立场tooltip
	const standpointTooltip = computed(() => {
		const { support, oppose, neutral, total } = standpointStats.value;
		if (total === 0) return "无立场数据";

		const supportPct = Math.round((support / total) * 100);
		const opposePct = Math.round((oppose / total) * 100);
		const neutralPct = Math.round((neutral / total) * 100);

		return `支持 ${supportPct}% | 中立 ${neutralPct}% | 反对 ${opposePct}%`;
	});

	// 立场图表样式
	const standpointStyle = computed(() => {
		const { support, oppose, neutral, total } = standpointStats.value;
		if (total === 0) return {};

		const supportHeight = Math.round((support / total) * 100);
		const neutralHeight = Math.round((neutral / total) * 100);
		const opposeHeight = Math.round((oppose / total) * 100);

		return {
			"--support-height": `${supportHeight}%`,
			"--neutral-height": `${neutralHeight}%`,
			"--oppose-height": `${opposeHeight}%`
		};
	});
</script>

<style scoped>
	.comment-stats {
		display: inline-flex;
		align-items: center;
		vertical-align: middle;
		gap: 4px;
		margin: 0 2px;
		line-height: inherit;
	}

	/* 迷你立场堆叠图 (纵向) */
	.standpoint-chart {
		display: inline-flex;
		align-items: flex-end;
		width: 8px;
		height: 16px;
	}

	.stacked-bar {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		gap: 1px;
	}

	.bar-segment {
		width: 100%;
		min-height: 1px;
		transition: height 0.2s ease;
	}

	.bar-segment.support {
		background-color: #ccebc5;
		height: var(--support-height, 0%);
	}

	.bar-segment.neutral {
		background-color: #b3cde3;
		height: var(--neutral-height, 0%);
	}

	.bar-segment.oppose {
		background-color: #fbb4ae;
		height: var(--oppose-height, 0%);
	}

	/* 类型饼图 - 确保垂直居中 */
	.type-pie-chart {
		display: inline-block;
		border-radius: 50%;
		vertical-align: middle;
		position: relative;
		top: 50%;
		transform: translateY(-60%);
	}
</style>
