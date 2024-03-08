<script lang="ts">
	import { onMount } from "svelte";
	import Download from "../../Components/DownloadPage.svelte";
	import Nav from "../../Components/NavBar.svelte";
	const urlBase: string = "http://127.0.0.1:8000/"
	let offline: boolean = true;
	async function doSomething(){
		try{
			const data = await fetch(urlBase);
			offline = false;
			return data;
		}catch(error){
			console.log("Promise failed, problem with backend. Is the backend running?");
			return;
		}
	}
	onMount(async () => {
		const a = doSomething();
		console.log(a);
	});
</script>

<main>
	<Nav topButtonText="Metadata" bottomButtonText="Training"/>
	{#if offline}
		<h1 id="offline">BACKEND OFFLINE!</h1>
	{:else}
		<Download />
	{/if}
</main>

<style>
	h1{
		color: #fff;
		text-shadow:
			2px 2px 0 #000,
			-2px 2px 0 #000,
			-2px -2px 0 #000,
			2px -2px 0 #000;
	}
	main {	
		position: relative;
		text-align: center;
		flex: 1;
		display: flex;
		flex-direction: column;
		font-size: 20px;
	}
</style>