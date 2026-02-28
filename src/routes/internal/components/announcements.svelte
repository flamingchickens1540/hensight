<script>
    let data = [
        {
            author: "Pit Admin",
            message: "the pits are burning down",
            time: "15m ago"
        },
        {
            author: "1844",
            message: "we need a 18x44 meter pizza",
            time: "40m ago"
        }
    ]
</script>

<div class="border-4 border-white rounded-lg size-full overflow-auto">
    <h1 class="p-1 text-[2.5rem]">Announcements</h1>
    {#each data as msg}
        <div class="border-3 border-white rounded-lg w-[80%] m-auto mb-1">
            <h1 class="text-[1.4rem] p-0.5">{msg.author}</h1>
            <p class="m-auto text-center text-[1.8rem]">{msg.message}</p>
            <p class="text-(--light-grey) text-[1.2rem] pl-0.5">{msg.time}</p>
        </div>
    {/each}
</div>