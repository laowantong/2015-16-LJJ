# encoding: utf8

from codecs import open
import unicodedata
from collections import defaultdict

def validate_sentences(path):
    lines = open(path, "r", "utf8").read().split("\n")
    result = set()
    print path
    for (i, line) in enumerate(lines, 1):
        if not line or line.startswith("//"):
            continue
        if line.count("\t") > 1:
            print "Line %s contains more than one tabulation." % i
            continue
        if line.count("\t") == 0:
            print "Line %s contains no tabulation." % i
            continue
        (chinese, translation) = line.split("\t")
        if not chinese:
            print "No chinese sentence in line %s." % i
            continue
        result.add(chinese)
        if not translation:
            print "No translation in line %s." % i
            continue
    print "%s sentences checked." % i
    return result

def validate_words(path, sentences):
    lines = open(path, "r", "utf8").read().split("\n")
    groups = defaultdict(list)
    print path
    for (i, line) in enumerate(lines, 1):
        if not line or line.startswith("//"):
            continue
        if line.count("\t") > 1:
            print "Line %s contains more than one tabulation." % i
            continue
        if line.count("\t") == 0:
            print "Line %s contains more than one tabulation." % i
            continue
        (chinese, stuff) = line.split("\t")
        if not chinese:
            print "No chinese word in line %s." % i
            continue
        if not stuff:
            print "Nothing after the chinese word in line %s." % i
            continue
        if stuff.count("|") > 1:
            print "Line %s contains more than one pipe symbol (|)." % i
            continue
        if stuff.count("|") == 0:
            print "Line %s contains no pipe symbol (|)." % i
            continue
        (pinyin, stuff) = stuff.split("|")
        if not pinyin:
            print "No pinyin in line %s." % i
            continue
        if not stuff.strip():
            print "Nothing after the pinyin in line %s." % i
            continue
        elements = [s.strip() for s in stuff.split("&")]
        translation = elements[0]
        if not translation:
            print "No translation in line %s." % i
            continue
        groups_and_examples = elements[1:]
        if not groups_and_examples:
            continue
        if not groups_and_examples[0]:
            print "Empty group or example in line %s." % i
            continue
        if unicodedata.category(groups_and_examples[0][0])!="Lo" and not groups_and_examples[0].startswith(("A:", u"“")):
            groups[groups_and_examples.pop(0)].append(i)
            if len(groups_and_examples):
                example = groups_and_examples.pop(0)
                if len(groups_and_examples):
                    print "More than one group and one example in line %s." % i
                    continue
            else:
                example = None
        else:
            example = groups_and_examples.pop(0)
            if len(groups_and_examples):
                print "More than one example in line %s." % i
                continue
        if example and example not in sentences:
            print "The example '%s' of line %s is absent from the base of sentences." % (example, i)
            continue
    for (group, lines) in groups.iteritems():
        if len(lines) == 1:
            print "Warning: group '%s' has only one occurrence in line %s." % (group, lines[0])
    print "%s words checked." % i

if __name__ == "__main__":
    sentences = validate_sentences("sentences_fr.txt")
    print
    validate_words("words_fr.txt", sentences)