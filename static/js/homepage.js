
document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("blois-video");
    const button = document.getElementById("blois-playback-toggle");

    if (!video || !button) return;

    const motionPreference = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    function updatePlaybackButton() {
        const isPlaying = !video.paused && !video.ended;

        button.setAttribute(
            "aria-label",
            `${isPlaying ? "Pause" : "Play"} Blois artwork video`
        );

        button.innerHTML = isPlaying
            ? '<i class="fa-solid fa-pause" aria-hidden="true"></i>'
            : '<i class="fa-solid fa-play" aria-hidden="true"></i>';
    }

    function playVideo() {
        const playPromise = video.play();

        if (playPromise !== undefined) {
            playPromise.catch(() => {
                updatePlaybackButton();
            });
        }
    }

    function togglePlayback() {
        if (video.paused) {
            playVideo();
        } else {
            video.pause();
        }
    }

    button.addEventListener("click", togglePlayback);
    video.addEventListener("click", togglePlayback);

    video.addEventListener("play", updatePlaybackButton);
    video.addEventListener("pause", updatePlaybackButton);
    video.addEventListener("ended", updatePlaybackButton);

    motionPreference.addEventListener("change", (event) => {
        if (event.matches) {
            video.pause();
        }
    });

    updatePlaybackButton();

    if (!motionPreference.matches) {
        playVideo();
    }
});
