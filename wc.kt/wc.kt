import java.io.File

fun main(args: Array<String>) {
    if (args.size == 1) {
        val fileName = args[0]
        var inWord = false
        var lines = 0
        var words = 0
        var chars = 0
        val file = File(fileName)
        for(line in file.readLines()) {
            lines++
            for (c in line) {
                chars++
                if (c.isWhitespace()) {
                    if (inWord) {
                        words++
                        inWord = false
                    }
                } else {
                    if (!inWord) {
                        inWord = true
                    }
                }
           }
        }
        if (inWord) {
            words++
        }
        println("$lines $words $chars $fileName")
    }
}

