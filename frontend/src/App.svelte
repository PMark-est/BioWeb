<script>
	let elem;
	let display = false;
	let newColor = "rgb(255, 0, 0)"
	const items1 = [{item: "piim", kogus: 1}, {item: "sai", kogus: 2}, {item: "vorst", kogus: 3}];
	const items2 = [
		{item: "šokolaad", kogus: 56}, {item: "kommid", kogus: 15}, {item: "jäätis", kogus: 12}, {item: "hapukoor", kogus: 77},
		{item: "šokolaad", kogus: 56}, {item: "kommid", kogus: 15}, {item: "jäätis", kogus: 12}, {item: "hapukoor", kogus: 77},
		{item: "šokolaad", kogus: 56}, {item: "kommid", kogus: 15}, {item: "jäätis", kogus: 12}, {item: "hapukoor", kogus: 77},
		{item: "šokolaad", kogus: 56}, {item: "kommid", kogus: 15}, {item: "jäätis", kogus: 12}, {item: "hapukoor", kogus: 77},
		{item: "šokolaad", kogus: 56}, {item: "kommid", kogus: 15}, {item: "jäätis", kogus: 12}, {item: "hapukoor", kogus: 77},
		{item: "šokolaad", kogus: 56}, {item: "kommid", kogus: 15}, {item: "jäätis", kogus: 12}, {item: "hapukoor", kogus: 77},
	];
	let selected = new Map()

	const handleClick = () =>{
		display = ! display;
		console.log(selected);
		selected.clear()
	}

	const onClick = (e) => {
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

	const submitDownload = (type) => {
		if(type === "all"){
			alert("all")
			console.log(items1);
		} else if (type === "selected"){
			alert("selected")
			for (const v of selected.values()){
				console.log(items1[v.id].item);
			}
		}
	}
</script>

<main>
	<h1>Enter bacterium name</h1>
	<form onsubmit="return false">
		<input bind:this={elem} id="searchBar" type="text">
		<input on:click={handleClick} id="searchConfirm" type="image" alt="not found" src="search.png" />
	</form>
	<div id="downloadBtns">
		<button on:click={() => submitDownload("all")} class="downloadBtn">Download all</button>
		<button on:click={() => submitDownload("selected")} class="downloadBtn">Download selected</button>
	</div>
	<ul >	
		{#if display}
			{#each items2 as item, i}
				<li><button id={i} on:click={(e) => onClick(e.target)} class="liBtn">{i} {item.item} - {item.kogus}</button></li>
			{/each}
		{:else}
			{#each items1 as item, i}
				<li><button id={i} on:click={(e) => onClick(e.target)} class="liBtn">{i} {item.item} - {item.kogus}</button></li>
			{/each}
	{/if}
	</ul>
</main>

<style>
	h1 {
		margin-top: 25vh;
	}
	main {	
		position: relative;
		text-align: center;
		flex: 1;
		display: flex;
		flex-direction: column;
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