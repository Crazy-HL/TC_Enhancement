<template>
	<span class="sentence-wrapper">
		<span
			class="sentence"
			:class="{
				'has-comment': hasComments,
				selected: isActive
			}"
			@click="handleClick">
			<span v-html="circledSentence"></span>
			<sup v-if="showMarker && hasComments" class="annotation-marker">
				{{ commentCount }}
			</sup>
		</span>
	</span>
</template>

<script setup>
	import { computed } from "vue";

	const props = defineProps({
		sentence: {
			type: String,
			required: true
		},
		sentenceIndex: {
			type: Number,
			required: true
		},
		highFrequencyWords: {
			type: Object,
			default: () => ({})
		},
		showHighlight: {
			type: Boolean,
			default: true
		},
		hasComments: {
			type: Boolean,
			default: false
		},
		commentLevel: {
			type: Object,
			default: () => ({ level: 0 })
		},
		isActive: {
			type: Boolean,
			default: false
		},
		showMarker: {
			type: Boolean,
			default: true
		},
		commentCount: {
			type: Number,
			default: 0
		},
		visibleCommentTypes: {
			type: Object,
			default: () => ({})
		}
	});

	const emit = defineEmits(["click"]);

	const escapeRegExp = string => {
		return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
	};

	const circledSentence = computed(() => {
		if (
			!props.showHighlight ||
			!props.highFrequencyWords[props.sentenceIndex]
		) {
			return props.sentence;
		}

		const keywords = [...props.highFrequencyWords[props.sentenceIndex]];
		let processed = props.sentence;

		keywords.sort((a, b) => b[1] - a[1]);

		// 处理前5个高频词
		keywords.slice(0, 5).forEach(([word]) => {
			if (props.sentence.includes(word)) {
				const regex = new RegExp(escapeRegExp(word), "g");
				processed = processed.replace(
					regex,
					`<span class="circled-word" title="高频词汇">${word}</span>`
				);
			}
		});

		return processed;
	});

	const handleClick = () => {
		emit("click", props.sentenceIndex);
	};
</script>

<style scoped>
	.sentence-wrapper {
		display: inline;
	}

	.sentence {
		display: inline;
		margin-right: 0.2em;
		position: relative;
		transition: all 0.2s;
		padding: 0 1px;
		cursor: pointer;
	}

	.sentence.has-comment {
		/* 无背景色 */
	}

	.sentence.selected {
		background-color: rgba(255, 236, 179, 0.4); /* 点击高亮效果 */
	}

	.annotation-marker {
		color: #ff9800;
		font-size: 0.8em;
		vertical-align: super;
		margin-left: 2px;
	}

	/* 高频词圆圈样式 - 使用固定颜色 */
	:deep(.circled-word) {
		position: relative;
		display: inline-block;
		padding: 0 2px;
		z-index: 1;
	}

	:deep(.circled-word::before) {
		content: "";
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: calc(100% + 8px);
		height: calc(100% + 4px);
		border: 2px solid #ffeb3b; /* 固定颜色 */
		border-radius: 50%;
		box-sizing: border-box;
		z-index: -1;
		opacity: 0.8;
		transition: all 0.3s ease;
	}

	:deep(.circled-word:hover::before) {
		opacity: 1;
		border-width: 3px;
		box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
	}
</style>
