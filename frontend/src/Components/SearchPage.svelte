<script lang="ts">
    import {listToMap, hash, getTaxa, getAntibiotics} from "../lib/helpers";
    import searchIcon from "../lib/search.png";
	const urlBase: string = "http://127.0.0.1:8000/"
	const newColor:string = "rgb(255, 0, 0)";
	let searchBarRef: HTMLInputElement;
	let antibiotics: Promise<Map<string, number>> | undefined;
	let selectedAntibiotics: Map<string, number> = new Map<string, number>();
	let downloading: boolean;
	let downloaded: number;
	let downloadAmount: number;
	let ID: number;

	async function handleClick(){
        const name: string = searchBarRef.value.toLowerCase();
        const nameHash: number = hash(name) % 101;
		const sessionStorageElem: string | null = sessionStorage.getItem(String(nameHash));
		if (sessionStorageElem != null){
			const map: Map<string, number> | PromiseLike<Map<string, number>> = listToMap(JSON.parse(sessionStorageElem)[1]);
				antibiotics = new Promise((resolve, reject) => {
				resolve(map);
			});
			ID = JSON.parse(sessionStorageElem)[0];
            return;
		}

		const id: number = await getTaxa(name);
		if (id === -1){
			antibiotics = undefined;
			return;
		}
		ID = id;
		antibiotics = getAntibiotics(id).then((list) => {
			sessionStorage.setItem(String(nameHash), JSON.stringify([id, list]));
			return listToMap(list);
		});
	}

	async function downloadFiles(selection: string[]){
		const name: string = searchBarRef.value.toLowerCase();
		const API = urlBase + "metadata";
		downloading = true;
		downloaded = 0;
		downloadAmount = selection.length;
		for(const s of selection){
			const data = {
				'bacterium': name,
				'antibiotic': s,
				'id': ID,
				'amount': (<HTMLInputElement>document.getElementById(s)).value,
			}
			await fetch(API, {
				method: 'POST',
				body: JSON.stringify(data)
			});
			downloaded++;
		}
		downloading = false;
	}

	const onClick = (e: any) => {
		const color = e.style.backgroundColor;
		const parts = e.id.split(",")
		if (color != newColor){
			e.style.backgroundColor = newColor;
			selectedAntibiotics.set(parts[0], parts[1]);
		}
		else{
			e.style.backgroundColor = "#fff";
			selectedAntibiotics.delete(parts[0]);
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
			downloadFiles(Array.from(selectedAntibiotics.keys()));
		}
	}

    const onFormSubmit = (e: SubmitEvent) => {
		selectedAntibiotics.clear();
        const formData = new FormData(e.target as HTMLFormElement);
    }
</script>

{#if downloading}
	<h1 class="downloading">DOWNLOADING... {downloaded}/{downloadAmount}</h1>
{:else if downloading === false}
	<h1 class="downloading">DOWNLOADED!</h1>
{/if}
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
	<h1>LOADING...</h1>
{:then items}
	{#if items === undefined}
		<h1>NO RESULTS FOUND</h1>
	{:else}
		<ul >	
			{#each [...items] as item}
			<li><button id={`${item[0]}`} value={item[1]} on:click={(e) => onClick(e.target)} class="liBtn">Antibiotic, Strains: {item[0]}, {item[1]}</button></li>
			{/each}
		</ul>
	{/if}
{:catch error}
	<h1>{error.message}</h1>
{/await}
<style>
	.downloading{
		position: absolute;
		width: 100%;
		text-align: center;
    	top: 10%;
	}
	h1{
		color: #fff;
		text-shadow:
			2px 2px 0 #000,
			-2px 2px 0 #000,
			-2px -2px 0 #000,
			2px -2px 0 #000;
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