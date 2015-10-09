"""
Test program for pre-processing schedule
"""
import arrow

base = arrow.now()

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  
    """
    field = None
    entry = { }
    cooked = [ ] 
    counter = 0

    for line in raw:
        line = line.rstrip()
        if len(line) == 0:
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line
            continue
        if len(parts) == 2:
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))


        if field == "begin":
            try:
                base = arrow.get(content, "M/D/YYYY")
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }

            #This code helps highlight the correct week
            entry['current'] = "OFF"
            theWeek = base.replace(weeks=+counter)
            nextWeek = base.replace(weeks=+(counter+1))
            if theWeek < arrow.now() < nextWeek:
                entry['current'] = "ON"

            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = "Week "+content+": "
            entry['date'] = theWeek.format('MM/DD/YYYY')

            #prepare for the next iteration through the loop
            counter += 1
            theWeek = theWeek.replace(weeks=+counter)

        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    return cooked


def main():
    f = open("static/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
