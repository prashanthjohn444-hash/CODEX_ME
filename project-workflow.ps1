Add-Type -AssemblyName System.Drawing
$canvas = [System.Drawing.Bitmap]::new(1600, 1320)
$g = [System.Drawing.Graphics]::FromImage($canvas)
$g.SmoothingMode = 'AntiAlias'
$g.TextRenderingHint = 'AntiAliasGridFit'
$g.Clear([System.Drawing.ColorTranslator]::FromHtml('#101827'))
$titleFont = [System.Drawing.Font]::new('Segoe UI', 30, [System.Drawing.FontStyle]::Bold)
$headingFont = [System.Drawing.Font]::new('Segoe UI', 19, [System.Drawing.FontStyle]::Bold)
$bodyFont = [System.Drawing.Font]::new('Segoe UI', 15)
$smallFont = [System.Drawing.Font]::new('Segoe UI', 13)
$white = [System.Drawing.Brushes]::White
$muted = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#bac9df'))
$pen = [System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml('#86a9d7'), 3)
$pen.CustomEndCap = [System.Drawing.Drawing2D.AdjustableArrowCap]::new(5, 6)
function Label($text, $x, $y, $font, $brush) { $g.DrawString($text, $font, $brush, [single]$x, [single]$y) }
function Box($x, $y, $w, $h, $title, $lines, $color = '#1e3048') {
    $brush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($color))
    $g.FillRectangle($brush, $x, $y, $w, $h)
    Label $title ($x+22) ($y+15) $headingFont $white
    $lineY = $y+53
    foreach ($line in $lines) { Label $line ($x+22) $lineY $bodyFont $muted; $lineY += 28 }
    $brush.Dispose()
}
function Arrow($x1,$y1,$x2,$y2) { $g.DrawLine($pen,$x1,$y1,$x2,$y2) }
Label 'PYTHON 30 DAYS | PROJECT WORKFLOW' 60 35 $titleFont $white
Label 'Mapped from project documents and build scripts | 19 October 2026' 62 93 $bodyFont $muted
Box 60 150 450 140 '1  Curriculum source' @('Original course HTML (external input)', 'extract_course.py -> source/lessons.json', '30 lessons + extracted source text')
Box 570 150 970 140 '2  Course planning and packaging' @('episode_data.json + build_pack.py + local .opencode skills', 'episodes/day-01.md ... day-30.md | titles, hooks, thumbnail briefs', '30-video-plan.md | production-tracker.csv | scores/ | research/')
Arrow 510 220 570 220
Arrow 1055 290 1055 330
Box 570 330 970 125 '3  Spoken script and production brief' @('day-01-spoken-script.md -> production/day-01/', 'v2/task-brief.md defines narration, real demonstrations and B-roll')
Arrow 1055 455 1055 480
$g.DrawLine($pen,1055,480,300,480)
$g.DrawLine($pen,1055,480,1300,480)
Arrow 300 480 300 515
Arrow 800 480 800 515
Arrow 1300 480 1300 515
Box 60 515 480 150 '4A  Narration' @('VoiceStudio / Adam (v2)', 'voice/v2/generate.py', 'Section WAVs + manifest.json') '#1b3b47'
Box 570 515 460 150 '4B  Real screen recordings' @('VS Code + Python via OBS', 'screen/v2/captures/', 'Demo code + capture manifests') '#1b3b47'
Box 1060 515 480 150 '4C  Explanatory graphics' @('B-roll scene definitions and builds', 'broll/v2/ -> rendered clips', 'HTML / HyperFrames / Remotion assets') '#1b3b47'
Arrow 300 665 300 700
Arrow 800 665 800 700
Arrow 1300 665 1300 700
$g.DrawLine([System.Drawing.Pens]::SlateGray,300,700,1300,700)
Arrow 800 700 800 735
Box 310 735 980 125 '5  Timeline and assembly' @('v2/timeline/edit-plan-v2.json: media paths, frames and cue points', 'Resolve build scripts / Console chunks | FFmpeg master renderer')
Arrow 800 860 800 895
Box 310 895 980 125 '6  Export and review' @('output/python-day-01-v2-master.mp4 exists', 'Review stills, manifests, verification scripts and delivery report') '#244139'
Label 'File existence confirmed; media quality was not revalidated in this inspection.' 335 1036 $smallFont $muted
Box 60 1090 710 125 'Related: course teaser' @('brag-output/ -> vertical Python course promo', 'Uses course identity and Day 1 material') '#332e47'
Box 800 1090 740 125 'Separate: abstract animation' @('videos/glass-red-white-grids/', 'Independent 8-second HyperFrames background loop') '#332e47'
Label 'Course scope: 30 lesson briefs; Day 1 has produced media. Publication and analytics are later stages.' 62 1245 $bodyFont $muted
$outPath = Join-Path $PSScriptRoot 'project-workflow.png'
$canvas.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$canvas.Dispose()
Write-Output $outPath
