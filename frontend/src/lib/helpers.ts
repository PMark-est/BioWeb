// Gets the id of a bacterium
export async function getTaxa(name: string): Promise<number> {
	if (name.length === 0) return 0;
	const nameParts: string[] = name.split(' ');
	const taxa = await fetch('https://www.bv-brc.org/api/taxonomy/', {
		method: 'POST',
		headers: {
			'Access-Control-Allow-Origin': '*',
			Accept: 'application/javascript, application/json, application/json',
			'Content-Type': ' application/rqlquery+x-www-form-urlencoded'
		},
		body: `and(keyword(${nameParts[0]}),keyword(${nameParts[1]}))&gt(genomes,1)&sort(-genomes)`
	}).then((resp) => resp.json());
	if (taxa.length === 0) return -1;
	for (let i: number = 0; i < taxa.length; i++) {
		if (taxa[i].taxon_rank === 'species') {
			return taxa[i].taxon_id;
		}
	}
	return -1;
}

export async function getAntibiotics(ID: number): Promise<string[]> {
	return fetch(
		`https://www.bv-brc.org/api/genome_amr/??and(eq(genome_id,*)&genome(eq(taxon_lineage_ids,${ID})),eq(evidence,%22Laboratory%20Method%22))&limit(1)&facet((field,antibiotic),(mincount,1),(limit,-1))`,
		{
			headers: { Accept: 'application/solr+json' }
		}
	)
		.then((resp) => resp.json())
		.then((resp) => {
			return resp.facet_counts.facet_fields.antibiotic;
		});
}

export function hash(string: string): number {
	let hash = 0;
	let char;
	if (string.length === 0) return hash;
	for (let i = 0; i < string.length; i++) {
		char = string.charCodeAt(i);
		hash = (hash << 5) - hash + char;
		hash |= 0;
	}
	return hash;
}

export function listToMap(list: string[]): Map<number, string> {
	let map = new Map();
	for (let i = 0; i < list.length; i += 2) map.set(list[i], list[i + 1]);
	return map;
}
