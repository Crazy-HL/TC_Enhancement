<template>
	<div class="high-freq-legend">
		<span class="legend-item">
			<!-- <span class="legend-label">高频词汇：</span> -->
			<span class="circled-word" style="--circle-color: #ffeb3b">高频词汇</span>
		</span>
	</div>
</template>

<script setup></script>

<style scoped>
	.high-freq-legend {
		display: flex;
		align-items: center;
		padding: 8px 12px;
		background: white;
		border-radius: 6px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		margin-right: 10px;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 14px;
		color: #555;
	}

	.legend-label {
		white-space: nowrap;
	}

	.circled-word {
		position: relative;
		display: inline-block;
		padding: 0 4px;
		z-index: 1;
	}

	.circled-word::before {
		content: "";
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: calc(100% + 8px);
		height: calc(100% + 4px);
		border: 2px solid var(--circle-color);
		border-radius: 50%;
		box-sizing: border-box;
		z-index: -1;
		opacity: 0.8;
	}
</style>
