import myaa.subkt.ass.*
import myaa.subkt.tasks.*
import myaa.subkt.tasks.Mux.*
import myaa.subkt.tasks.Nyaa.*
import java.awt.Color
import java.time.*

plugins {
    id("myaa.subkt")
}

subs {
    readProperties("sub.properties", "private.properties")
    episodes(getList("episodes"))

    merge {
        from(get("dialogue")) {
            incrementLayer(10)
        }
        from(getList("typesets"))
        from(get("insert"))
        from(get("ending"))
    }

    mux {
        title(get("title"))

        from(get("premux")) {
            video {
                name("BD 1080p HEVC [dedsec]")
                lang("ita")
                default(true)
            }

            audio {
                name("Japanese 5.1 AAC")
                lang("jpn")
                default(true)
            }

            attachments {
                include(false)
            }
        }

        from(merge.item()) {
            tracks {
                name("Kaizoku")
                lang("eng")
                default(true)
            }
        }

        chapters(get("chapters")) {
            lang("eng")
            charset("UTF-8")
        }

        attach(get("fonts")) {
            includeExtensions("ttf", "otf")
        }

        skipUnusedFonts(true)
        out(get("muxfile"))
    }
}
