# Public-video reference — yt-viral

Observed through public YouTube search results on **2026-10-08**. The recorded counts are indexed public counts and may lag the live pages. All five sampled videos are from Corey Schafer's beginner series and show the same publication date, 2017-05-17.

The sample was selected for comparable beginner topics, not collected as a complete channel catalog. Its median is **1,796,597 views**. Multiples below are relative to this **five-video sample**, not a measured median of the entire channel. This is evergreen reference research, not a current-trend ranking or a Telugu-market study.

| Rank | Video | Observed views | Sample-median multiple | Tool formula |
| --- | --- | ---: | ---: | --- |
| 1 | [Install and Setup for Mac and Windows](https://www.youtube.com/watch?v=YYXdXT2l-Gg) | 4,357,630 | 2.43× | Unclassified |
| 2 | [Strings — Working with Textual Data](https://www.youtube.com/watch?v=k9TUPpGqYTo) | 2,147,599 | 1.20× | Unclassified |
| 3 | [Dictionaries — Working with Key-Value Pairs](https://www.youtube.com/watch?v=daefaLgNkw0) | 1,796,597 | 1.00× | Unclassified |
| 4 | [Functions](https://www.youtube.com/watch?v=9Os0o3wzS_I) | 1,350,801 | 0.75× | Unclassified |
| 5 | [Conditionals and Booleans](https://www.youtube.com/watch?v=DZwmZ8Usvnk) | 836,461 | 0.47× | Unclassified |

The installed `swipe.py` was run with a **2.0× threshold**. Only the setup video clears it; there are not five qualifying outliers in this sample. Raw input is in [public-videos.json](public-videos.json), and the actual tool result is in [outliers.json](outliers.json).

**Shared structural feature:** each title names a beginner concept and usually clarifies the practical subject. The formula classifier finds none of its 21 keyword patterns; “Unclassified” is a tool result, not a judgment of video quality. The sample does not establish why any video received its views. A first episode may also benefit from being the entry point to a series.

**What you can make this week:** a setup video that leads with a running file and resolves the shell-versus-script confusion. Your HTML already supplies installation, shell, syntax-error, data-type, and file material. The course-specific mind map and follow-along lab are useful presentation assets.

For a broader comparison, collect at least four comparable videos per channel, preferably more, with URLs, observation dates, publication dates, durations, and counts. Separate Shorts from long-form and recent uploads from years-old videos. If the course language is Telugu, build a Telugu-specific comparison before drawing audience-specific conclusions.

```powershell
python .opencode/skills/yt-viral/swipe.py youtube-course/research/public-videos.json --min 2.0 --json
```

ship it, or change it?
