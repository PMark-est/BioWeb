<script lang="ts">
    import {listToMap, hash, getTaxa, getAntibiotics} from "../lib/helpers";
    import searchIcon from "../lib/search.png";
    const test:number = 3;
	const newColor:string = "rgb(255, 0, 0)";
    const tempStore:Map<number, Map<number, string>> = new Map();
	let elem: any;
	let display: boolean = false;
    let items: Map<number, string> | undefined = new Map();
	let selected: Map<number, string> = new Map();

	const handleClick = () =>{
        const name: string = elem.value.toLowerCase();
        const nameHash: number = hash(name) % 101;
        if (tempStore.has(nameHash)){
            items = tempStore.get(nameHash);
            display = true;
            return;
        };
        getTaxa(name).then((id) => {
            display = false;
            if (id == -1){
                return;
            };
            getAntibiotics(id).then((resp) => {
                items = listToMap(resp);
                tempStore.set(nameHash, items);
                display = true;
                console.log(items);
            });
        });
	}

	const onClick = (e: any) => {
		let color = e.style.backgroundColor;
		if (color != newColor){
			e.style.backgroundColor = newColor;
			selected.set(e.id, e)
		}
		else{
			e.style.backgroundColor = "#000";
			selected.delete(e.id);
		}
	}

	const submitDownload = (type: any) => {
		if(type === "all"){
			alert("all")
			console.log(items);
		} else if (type === "selected"){
			alert("selected")
			for (const v of selected.values()){
				//console.log(items[v.id].item);
			}
		}
	}

    const onFormSubmit = (e: SubmitEvent) => {
        const formData = new FormData(e.target as HTMLFormElement);
    }
</script>

<h1>Enter bacterium name</h1>
<form on:submit|preventDefault="{onFormSubmit}">
    <input bind:this={elem} id="searchBar" type="text">
    <input on:click={handleClick} id="searchConfirm" type="image" alt="not found" src={searchIcon} />
</form>
<div id="downloadBtns">
    <button on:click={() => submitDownload("all")} class="downloadBtn">Download all</button>
    <button on:click={() => submitDownload("selected")} class="downloadBtn">Download selected</button>
</div>
<ul >	
    {#if display}
        {#each [...items] as item, i}
        <li><button id={String(i)} on:click={(e) => onClick(e.target)} class="liBtn">Antibiotic, Strains: {item[0]}, {item[1]}</button></li>
        {/each}
	{/if}
</ul>
<style>
	h1 {
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
		background-color: #000;
		color: #fff;
	}
</style>