<script>
    let nowQueue = "QM3"
    let onField = "QM1"
    let lunch = "15:40"
</script>

<div class="border-4 border-(--color-white) rounded-lg size-full">
    <h1 class="p-1 text-[2.5rem]">Event</h1>
    <div class="flex flex-col w-[80%] m-auto justify-center gap-1 text-center text-[2.5rem]">
        <h1 class="flex justify-center gap-1">Now Queueing: <p class="font-medium">{nowQueue}</p></h1>
        <h1 class="flex justify-center gap-1">On Field: <p class="font-medium">{onField}</p></h1>
        <h1 class="flex justify-center gap-1">Lunch: <p class="font-medium">{lunch}</p></h1>
    </div>
</div>