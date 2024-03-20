<script lang="ts">
	import { onMount } from "svelte";
    import backIcon from "../lib/back.png";
    const newColor:string = "rgb(255, 0, 0)";
    const urlBase: string = "http://127.0.0.1:8000/"
	let ref: HTMLInputElement | undefined;
    let prm: Promise<string[]> = new Promise((resolve, reject) => {
        resolve([]);
    });
    let fileView:boolean = false;
    let downloading: boolean = false;
    let collectingData: boolean = false;
    let displayPopup: boolean = false;
    let bacterium: string = "";
    let antibiotic: string = "";
    let res: number;
    let sus: number;
    async function getFolders(){
        prm = fetch(urlBase+"viewf")
        .then((resp) => resp.json())
        .then((resp) => {
            return resp.folders;
        });
    }

    onMount(() => {
        getFolders()
    })

    function shake(resInput: HTMLInputElement, susInput: HTMLInputElement){
        const resValue: number = Number(resInput?.value);
        const susValue: number = Number(susInput?.value);
        const resShake: boolean = resValue > res || resValue < 0;
        const susShake: boolean = susValue > sus || susValue < 0;
        if (resShake){
            resInput.style.border = "3px solid #f00";
            resInput.animate([
            { transform: 'translateY(0px)' },
            { transform: 'translateX(-10px)' },
            { transform: 'translateX(10px)' },
            { transform: 'translateX(0px)' }
            ], {
            duration: 150,
            iterations: 1,
            });
        }
        if (susShake){
            susInput.style.border = "3px solid #f00";
            susInput.animate([
            { transform: 'translateY(0px)' },
            { transform: 'translateX(-10px)' },
            { transform: 'translateX(10px)' },
            { transform: 'translateX(0px)' }
            ], {
            duration: 150,
            iterations: 1,
        });
        }
        if (!resShake) resInput.style.border = "none";
        if (!susShake) susInput.style.border = "none";
        if(resShake || susShake || (resValue + susValue === 0)) return true;
        return false;
    }

    async function print(reader: any, amount:number){
        const progressbar = document.getElementById("progressbar");
        if (!progressbar) return;
        const decoder: TextDecoder = new TextDecoder();
        var text: string;
        const { done, value } = await reader.read();
        collectingData = false;
        text = (decoder.decode(value));
        var progress: number = 0;
        while (true){
            const { done, value } = await reader.read();
            text = (decoder.decode(value));
            progress += Number(decoder.decode(value));
            if (done) break;
            progressbar.style.width = `${progress}%`;
        }
    }

    async function download(){
        if (downloading){
            displayPopup = true;
            return;
        }
        const resBtn: HTMLInputElement = <HTMLInputElement>document.getElementById("res");
        const susBtn: HTMLInputElement = <HTMLInputElement>document.getElementById("sus");
        const resValue: number = Number(resBtn?.value);
        const susValue: number = Number(susBtn?.value);
        if(shake(resBtn, susBtn)) return;
        collectingData = true;
        downloading = true;
        const response = await fetch(urlBase+"stream?bacterium="+bacterium+"&antibiotic="+antibiotic+"&resAmount="+resValue+"&susAmount="+susValue);
        const reader = response.body?.getReader();
        if (!reader) return;
        await print(reader, resValue+susValue);
        downloading = false;
    }

    function antibioticSelected(e: any){
        if (!fileView){
            bacterium = e.id;
            fileView = true;
            fetch(urlBase+`viewc?bacterium=${e.textContent}`)
            .then((resp) => resp.json())
            .then((resp) => {
                prm = resp.files;
            });
            return;
        }
        const color = e.style.backgroundColor;
        const parts = e.id.split(",")
        antibiotic = parts[0];
        res = Number(parts[1]);
        sus = Number(parts[2]);
		if (color != newColor) e.style.backgroundColor = newColor;
		else e.style.backgroundColor = "#fff";

        if (ref) ref.style.backgroundColor = "#fff";
        ref = e;
        
    }

    function toFolderView(){
        fileView = false;
        getFolders()
    }

    function disablePopup() {
        displayPopup = false;
    }
</script>

<div id="body">
    <div id="list">
        {#if fileView}
        <div id="fileView">
            <input on:click={toFolderView} id="back" type="image" alt="not found" src={backIcon} />
            <p>antibiotic, resistants, susceptibles</p>
        </div>
        {/if}
        {#await prm}
        {:then items}
        {#if items !== undefined}
        <ul >	
            {#each [...items] as item}
            <li><button id={`${item}`} class="liBtn" on:click={(e) => antibioticSelected(e.target)}>{item}</button></li>
            {/each}
        </ul>
        {/if}
        {:catch error}
        <h1>{error.message}</h1>
        {/await}
    </div>

    <div id="menu">
        <div id="inputs">
            <span>
                <h1>RESISTANTS</h1>
                <input id="res" type="number" value="0">
            </span>
            <span>
                <h1>SUSCEPTIBLES</h1>
                <input id="sus" type="number" value="0">
            </span>
        </div>
        <button on:click={download} id="downloadBtn">DOWNLOAD GENOMES</button>
        {#if collectingData}
            <h1>COLLECTING DATA...</h1>
        {/if}
        <div id="progressbarWrapper">
            <div id="progressbar">
            </div>
        </div>
    </div>
</div>
{#if displayPopup}
    <div id="popup">
        <h1>THERE ARE ITEMS ALREADY BEING DOWNLOADED</h1>
        <button on:click={disablePopup}>CLOSE</button>
    </div>
{/if}


<style>
    #popup{
        position: absolute;
        background-color: #0008;
        top: -8px;
        left: -8px;
        width: 100vw;
        height: 100vh;
    }
    #popup h1{
        text-shadow: -1px 0 #fff,
            1px 0 #fff,
            0 1px #fff,
            0 -1px #fff;
    }

    #popup button{
        width: 100px;
    }

    input{
        text-align: center;
    }
    input:focus{
        outline: none;
    }
    #progressbarWrapper{
        position: relative;
        margin-top: 100px;
        width: 80%;
        height: 50px;
    }
    #progressbar{
        width: 0;
        height: 100%;
        background-color: #3fea78;
    }
    #body{
        display: flex;
        height: 60%;
    }
    #menu{
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: #fffa;
        width: 100px;
        height: 100%;
        flex: 1;
        margin: 6% 6% 0 0;
        box-shadow: 0 0 5px 10px #fffa;

    }
    #downloadBtn{
        width: 40%;
    }
    #inputs{
        display: flex;
        width: 100%;
        justify-content: space-around;
        margin-bottom: 50px;
    }
    p{
        color: #fff;
        text-shadow:
                1px 1px 0 #000,
                -1px 1px 0 #000,
                -1px -1px 0 #000,
                1px -1px 0 #000;
    }
    #list{
        width: 20%;
        height: 100%;
        margin: 100px 10% 30px 12%;
        overflow-y: auto;
        list-style: none;
        scrollbar-width: none; /* for firefox, ie, and edge */
    }

    #back{
        float: left;
        width: 50px;
        height: 50px;
    }

    ul{
        width: 100%;
        flex: 1;
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
        padding: 15px;
        width: 100%;
        height: 100%;
        border-radius: 10px;
        background-color: #fff;
        color: #000;
    }
</style>