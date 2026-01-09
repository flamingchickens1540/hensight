function msToHMS( ms: number ) {
    let seconds = ms / 1000;
    const hours = seconds / 3600;
    seconds = seconds % 3600;
    const minutes = seconds / 60;
    seconds = seconds % 60;
    return hours+":"+minutes+":"+seconds;
}