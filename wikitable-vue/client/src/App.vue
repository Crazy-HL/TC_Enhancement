<script>
	import ArticleContent from "./components/ArticleContent.vue";
	export default {
		name: "App",
		components: { ArticleContent },
		mounted() {
			// this.getData();
		},
		data() {
			return {
				// article: null,
				// comments: []
			};
		},
		methods: {
			// getData() {
			// 	api.get("article", {}, data => {
			// 		this.article = data;
			// 		// console.log("content:", data);
			// 	});
			// 	api.get("comments", {}, data => {
			// 		this.comments = data;
			// 		// console.log("comments", data);
			// 	});
			// }
		}
	};
</script>

<template>
	<ArticleContent />
	<!-- <CommentList /> -->
</template>

<style scoped></style>
