<script lang="ts">
    import {listToMap, hash, getTaxa, getAntibiotics} from "../lib/helpers";
    import searchIcon from "../lib/search.png";
	const newColor:string = "rgb(255, 0, 0)";
	let searchBarRef: HTMLInputElement;
	let antibiotics: Promise<Map<string, number>> | undefined;
	let selectedAntibiotics: Set<string> = new Set<string>();

	async function handleClick(){
        const name: string = searchBarRef.value.toLowerCase();
        const nameHash: number = hash(name) % 101;
		const sessionStorageElem: string | null = sessionStorage.getItem(String(nameHash));
		if (sessionStorageElem != null){
			const map: Map<string, number> | PromiseLike<Map<string, number>> = listToMap(JSON.parse(sessionStorageElem));
				antibiotics = new Promise((resolve, reject) => {
				resolve(map);
			});
            return;
		}

		const id: number = await getTaxa(name);
		if (id === -1){
			antibiotics = undefined;
			return;
		}
		antibiotics = getAntibiotics(id).then((list) => {
			sessionStorage.setItem(String(nameHash), JSON.stringify(list));
			return listToMap(list);
		});
	}

	async function downloadFile(antibiotic: string){
		console.log(antibiotic);
	}

	async function downloadFiles(selection: string[]){
		for(const s of selection){
			downloadFile(s);
		}
	}

	const onClick = (e: any) => {
		let color = e.style.backgroundColor;
		if (color != newColor){
			e.style.backgroundColor = newColor;
			selectedAntibiotics.add(e.id);
		}
		else{
			e.style.backgroundColor = "#fff";
			selectedAntibiotics.delete(e.id);
		}
	}

	const submitDownload = (type: any) => {
		if(type === "all"){
			if (antibiotics == null) return;
			antibiotics.then((resp) => {
				downloadFiles(Array.from(resp.keys()));
			});
		} else if (type === "selected"){
			if (selectedAntibiotics.size === 0) return;
			downloadFiles(Array.from(selectedAntibiotics));
		}
	}

    const onFormSubmit = (e: SubmitEvent) => {
        const formData = new FormData(e.target as HTMLFormElement);
    }
</script>

<h1 id="name">ENTER BACTERIUM NAME</h1>
<form on:submit|preventDefault="{onFormSubmit}">
    <input bind:this={searchBarRef} id="searchBar" type="text">
    <input on:click={handleClick} id="searchConfirm" type="image" alt="not found" src={searchIcon} />
</form>
<div id="downloadBtns">
    <button on:click={() => submitDownload("all")} class="downloadBtn">Download all</button>
    <button on:click={() => submitDownload("selected")} class="downloadBtn">Download selected</button>
</div>
	{#await antibiotics}
		<p>waiting...</p>
	{:then items}
		{#if items === undefined}
			<h1>NO RESULTS FOUND</h1>
		{:else}
			<ul >	
				{#each [...items] as item}
				<li><button id={item[0]} on:click={(e) => onClick(e.target)} class="liBtn">Antibiotic, Strains: {item[0]}, {item[1]}</button></li>
				{/each}
			</ul>
		{/if}
	{:catch error}
		<p>{error.message}</p>
	{/await}
<style>
	h1{
		color: #fff;
		text-shadow:
			2px 2px 0 #000,
			-2px 2px 0 #000,
			-2px -2px 0 #000,
			2px -2px 0 #000;
	}
	.routes {
        display: flex;
        flex-direction: column;
        align-items: baseline;
	}
	.routes button{
		width: 200px;
	}
	#name {
		margin-top: 25vh;
	}
	form{
		display: flex;
		gap: 60px;
		margin: 0 auto;
		width: 50%;
		height: 50px;
		margin-bottom: 10px;
	}
	#searchConfirm{
		width: 50px;
		height: 50px;
		padding: 0;
	}
	#searchBar{
		flex: 1;
		height: 50px;
		padding: 10px;
		text-align: center;
	}

	#downloadBtns{
		display: flex;
		margin: 0 auto;
		gap: 100px;
		width: 50%;
		margin-bottom: 30px;
	}

	.downloadBtn{
		width: 100%;
	}
	
	ul{
		flex: 1;
		overflow-y: auto;
		scrollbar-width: none; /* for firefox, ie, and edge */
		columns: 2;
		list-style: none;
		margin: 0 10% 30px 10%;
		padding: 0;
	}

	ul::-webkit-scrollbar{
		display: none;
	}
	
	li{
		font-size: 25px;
		margin-bottom: 10px;
	}

	.liBtn{
		margin: 0;
		padding: 20px;
		width: 100%;
		height: 100%;
		border-radius: 10px;
		background-color: #fff;
		color: #000;
	}
</style>