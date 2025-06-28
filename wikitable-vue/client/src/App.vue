<script>
	import api from "./api";
	import ArticleContent from "./components/ArticleContent.vue";
	import CommentList from "./components/CommentList.vue";
	export default {
		name: "App",
		components: { ArticleContent, CommentList },
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
	<CommentList />
</template>

<style scoped></style>
