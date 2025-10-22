<script>
    var data = [{title: "", red: "", blue: ""}]

    async function getData() {
        const request = await fetch("http://127.0.0.1:5003/getSchedule")
        data = await request.json()
    }
    getData() 

</script>

<div class="border-4 border-(--color-white) rounded-lg size-full overflow-auto">
    <h1 class="p-1 text-[2.5rem]">Schedule</h1>
    {#each data as match}
        <div class="text-[1.7rem] text-center flex flex-row justify-evenly"><h1>{match.title}: </h1><p class="text-(--color-red)">{match.red}</p><p class="text-(--color-blue)">{match.blue}</p></div>
    {/each}
</div>