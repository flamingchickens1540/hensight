<div class="grid-container">
    <div class="item" style="grid-row: 1 / span 3; grid-column: 1 / span 1;"></div>
    <div class="item" style="grid-row: 1 / span 2; grid-column: 2 / span 2;"></div>
    <div class="item" style="grid-row: 2 / span 3; grid-column: 4 / span 1;"></div>
    <div class="item" style="grid-row: 1 / span 1; grid-column: 4 / span 1;"></div>
    <div class="item" style="grid-row: 4 / span 1; grid-column: 1 / span 2;"></div>
    <div class="item" style="grid-row: 3 / span 1; grid-column: 2 / span 2;"></div>
    <div class="item" style="grid-row: 4 / span 1; grid-column: 3 / span 1;"></div>
</div>

<style>
    .item {
        background-color: var(--white);
        border-radius: 2.5rem;
        align-self: stretch;
        justify-self: stretch;
    }

    .grid-container {
        display: grid;
        position: fixed;
        width: 90%;
        height: 85%;
        left: 5%;
        top: 3%;
        margin: auto;
        row-gap: 1.25rem;
        column-gap: 20px;
        grid-template-rows: repeat(4,minmax(0,1fr));
        grid-template-columns: repeat(4,minmax(0,1fr));
    }
</style>