import React, { useState, useEffect } from "react";
import { Copy } from "lucide-react";

export default function VideoPreview({ url, transcript, setTranscript, setTitle }) {
  const [copied, setCopied] = useState(false);

  const getYouTubeId = (ytUrl) => {
    if (!ytUrl) return null;
    try {
      if (ytUrl.includes("youtu.be/"))
        return ytUrl.split("youtu.be/")[1].split(/[?&]/)[0];
      if (ytUrl.includes("youtube.com/watch"))
        return new URL(ytUrl).searchParams.get("v");
      if (ytUrl.includes("youtube.com/embed/"))
        return ytUrl.split("embed/")[1].split(/[?&]/)[0];
      if (ytUrl.includes("youtube.com/shorts/"))
        return ytUrl.split("shorts/")[1].split(/[?&]/)[0];
      return null;
    } catch {
      return null;
    }
  };

  const videoId = getYouTubeId(url);

  useEffect(() => {
    if (!url) return;

    const fetchTranscriptAndTitle = async () => {
      try {
        // Fetch transcript only if not already loaded
        if (!Array.isArray(transcript) || transcript.length === 0) {
          const response = await fetch(
            `http://localhost:8000/transcript/?url=${encodeURIComponent(url)}`
          );
          const data = await response.json();

          if (data.transcript && Array.isArray(data.transcript)) {
            setTranscript(data.transcript);
          } else {
            setTranscript([{ time: "00:00", text: "Transcript not available" }]);
          }
        }

        // Fetch video title
        const resTitle = await fetch(
          `https://www.youtube.com/oembed?url=${encodeURIComponent(url)}&format=json`
        );

        if (resTitle.ok) {
          const titleData = await resTitle.json();
          setTitle(titleData.title || "YouTube Video");
        } else {
          setTitle("YouTube Video");
        }
      } catch (error) {
        console.error("Error fetching transcript or title:", error);
        setTranscript([{ time: "00:00", text: "Error fetching transcript" }]);
        setTitle("YouTube Video");
      }
    };

    fetchTranscriptAndTitle();
  }, [url]);

  const handleCopyAll = () => {
    const textToCopy =
      transcript
        ?.map((line) => `${line.time} - ${line.text}`)
        .join("\n") || "";

    navigator.clipboard.writeText(textToCopy);
    setCopied(true);

    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col p-2 border-r md:w-full w-[250px] border-gray-700">
      {/* Video Player */}
      <div className="aspect-video min-h-[200px] w-full bg-black rounded-lg overflow-hidden">
        {videoId ? (
          <iframe
            src={`https://www.youtube.com/embed/${videoId}`}
            title="YouTube video"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="w-full h-full"
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            Paste a valid YouTube link to preview
          </div>
        )}
      </div>

      {/* Transcript Section */}
      <div className="mt-4">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-lg font-semibold">Transcript</h2>

          <button
            onClick={handleCopyAll}
            className="flex items-center gap-1 px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded text-sm"
          >
            {copied ? (
              <span className="text-green-400">Copied!</span>
            ) : (
              <>
                <Copy className="w-4 h-4" /> Copy All
              </>
            )}
          </button>
        </div>

        <div className="max-h-85 overflow-y-auto space-y-2 [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden">
          {Array.isArray(transcript) && transcript.length > 0 ? (
            transcript.map((line, i) => (
              <div
                key={i}
                className="p-2 bg-black overflow-hidden max-h-14 rounded-lg"
              >
                <span className="text-sm text-blue-400 mr-2">{line.time}</span>
                <span>{line.text}</span>
              </div>
            ))
          ) : (
            <div className="text-gray-400">No transcript available.</div>
          )}
        </div>
      </div>
    </div>
  );
}