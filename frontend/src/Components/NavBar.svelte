<script lang="ts">
    export let topButtonText: string;
    export let bottomButtonText: string;
    let routeTop: string;
    let routeBottom: string;
    switch(topButtonText){
        case "Download Page": routeTop = "/download"; break;
        case "Metadata": routeTop = "/"; break;
    }
    switch(bottomButtonText){
        case "Training": routeBottom = "/training"; break;
        case "Metadata": routeBottom = "/"; break;
    }
</script>

<div class="routes">
    <a href={routeTop}><button>{topButtonText}</button></a>
    <a href={routeBottom}><button>{bottomButtonText}</button></a>
</div>

<style>
    .routes {
        display: flex;
        flex-direction: column;
        align-items: baseline;
	}
    .routes button{
		width: 200px;
	}
</style>