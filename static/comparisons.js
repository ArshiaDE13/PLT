/* Cross-language comparison snippets for the "⇄ Compare" feature.
   Each topic has a bilingual label and the same tiny program written in
   each language the site teaches (code stays ASCII/LTR by design). */
window.COMPARISON_TOPICS = [
  {
    id: "hello",
    en: "Hello, World!",
    fa: "سلام، دنیا!",
    code: {
      python: 'print("Hello, World!")',
      c: '#include <stdio.h>\n\nint main(void) {\n    printf("Hello, World!\\n");\n    return 0;\n}',
      cpp: '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!\\n";\n    return 0;\n}',
      js: 'console.log("Hello, World!");',
    },
  },
  {
    id: "variables",
    en: "Variables",
    fa: "متغیرها",
    code: {
      python: 'age = 25            # no type declaration\name = "Ada"\npi = 3.14',
      c: '#include <stdio.h>\n\nint main(void) {\n    int age = 25;\n    char name[] = "Ada";\n    double pi = 3.14;\n    return 0;\n}',
      cpp: '#include <iostream>\n#include <string>\n\nint main() {\n    int age = 25;\n    std::string name = "Ada";\n    double pi = 3.14;\n}',
      js: 'let age = 25;          // let: can change\nconst name = "Ada";   // const: fixed\nlet pi = 3.14;',
    },
  },
  {
    id: "conditionals",
    en: "If / Else",
    fa: "شرط if / else",
    code: {
      python: 'score = 85\n\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelse:\n    print("C")',
      c: '#include <stdio.h>\n\nint main(void) {\n    int score = 85;\n    if (score >= 90) printf("A\\n");\n    else if (score >= 80) printf("B\\n");\n    else printf("C\\n");\n    return 0;\n}',
      cpp: '#include <iostream>\n\nint main() {\n    int score = 85;\n    if (score >= 90) std::cout << "A\\n";\n    else if (score >= 80) std::cout << "B\\n";\n    else std::cout << "C\\n";\n}',
      js: 'const score = 85;\n\nif (score >= 90) {\n  console.log("A");\n} else if (score >= 80) {\n  console.log("B");\n} else {\n  console.log("C");\n}',
    },
  },
  {
    id: "loops",
    en: "Loops",
    fa: "حلقه‌ها",
    code: {
      python: 'for i in range(1, 6):\n    print(i, "squared =", i * i)',
      c: '#include <stdio.h>\n\nint main(void) {\n    for (int i = 1; i <= 5; i++)\n        printf("%d squared = %d\\n", i, i * i);\n    return 0;\n}',
      cpp: '#include <iostream>\n\nint main() {\n    for (int i = 1; i <= 5; i++)\n        std::cout << i << " squared = " << i * i << "\\n";\n}',
      js: 'for (let i = 1; i <= 5; i++) {\n  console.log(`${i} squared = ${i * i}`);\n}',
    },
  },
  {
    id: "while",
    en: "While Loop",
    fa: "حلقهٔ while",
    code: {
      python: 'n = 3\nwhile n > 0:\n    print(n)\n    n -= 1\nprint("liftoff!")',
      c: '#include <stdio.h>\n\nint main(void) {\n    int n = 3;\n    while (n > 0) {\n        printf("%d\\n", n);\n        n--;\n    }\n    printf("liftoff!\\n");\n    return 0;\n}',
      cpp: '#include <iostream>\n\nint main() {\n    int n = 3;\n    while (n > 0) {\n        std::cout << n << "\\n";\n        n--;\n    }\n    std::cout << "liftoff!\\n";\n}',
      js: 'let n = 3;\nwhile (n > 0) {\n  console.log(n);\n  n--;\n}\nconsole.log("liftoff!");',
    },
  },
  {
    id: "functions",
    en: "Functions",
    fa: "توابع",
    code: {
      python: 'def add(a, b):\n    return a + b\n\nprint(add(2, 3))   # 5',
      c: '#include <stdio.h>\n\nint add(int a, int b) {\n    return a + b;\n}\n\nint main(void) {\n    printf("%d\\n", add(2, 3));   // 5\n    return 0;\n}',
      cpp: '#include <iostream>\n\nint add(int a, int b) {\n    return a + b;\n}\n\nint main() {\n    std::cout << add(2, 3);   // 5\n}',
      js: 'function add(a, b) {\n  return a + b;\n}\n\nconst addArrow = (a, b) => a + b;\nconsole.log(addArrow(2, 3));   // 5',
    },
  },
  {
    id: "lists",
    en: "Lists / Arrays",
    fa: "لیست‌ها و آرایه‌ها",
    code: {
      python: 'scores = [72, 95, 88]\nscores.append(100)\nprint(len(scores), scores[0])   # 4 72',
      c: '#include <stdio.h>\n\nint main(void) {\n    int scores[] = {72, 95, 88};\n    int n = 4;  /* arrays cannot grow: fix the size first */\n    printf("%d %d\\n", n, scores[0]);\n    return 0;\n}',
      cpp: '#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> scores = {72, 95, 88};\n    scores.push_back(100);   // grows!\n    std::cout << scores.size() << " " << scores[0];\n}',
      js: 'const scores = [72, 95, 88];\nscores.push(100);   // grows!\nconsole.log(scores.length, scores[0]);',
    },
  },
  {
    id: "strings",
    en: "Strings",
    fa: "رشته‌ها",
    code: {
      python: 'name = "Ada Lovelace"\nprint(name.upper())\nprint(name[4:9])     # "Lovel"\nprint(len(name))',
      c: '#include <stdio.h>\n#include <string.h>\n\nint main(void) {\n    char name[] = "Ada Lovelace";\n    printf("%zu %c\\n", strlen(name), name[4]);\n    return 0;\n}',
      cpp: '#include <iostream>\n#include <string>\n\nint main() {\n    std::string name = "Ada Lovelace";\n    std::cout << name.length() << " " << name.substr(4, 5);\n}',
      js: 'const name = "Ada Lovelace";\nconsole.log(name.toUpperCase());\nconsole.log(name.slice(4, 9));    // "Lovel"\nconsole.log(name.length);',
    },
  },
  {
    id: "oop",
    en: "Classes / Structs",
    fa: "کلاس‌ها و structها",
    code: {
      python: 'class Player:\n    def __init__(self, name, hp):\n        self.name = name\n        self.hp = hp\n\n    def hit(self, dmg):\n        self.hp -= dmg\n\np = Player("Ada", 100)\np.hit(30)\nprint(p.hp)   # 70',
      c: '#include <stdio.h>\n\ntypedef struct {\n    char name[20];\n    int hp;\n} Player;\n\nint main(void) {\n    Player p = {"Ada", 100};\n    p.hp -= 30;\n    printf("%d\\n", p.hp);   /* structs hold data, not methods */\n    return 0;\n}',
      cpp: '#include <iostream>\n#include <string>\n\nclass Player {\npublic:\n    Player(std::string n, int hp) : name(n), hp(hp) {}\n    void hit(int dmg) { hp -= dmg; }\n    int hp() const { return hp; }\n    std::string name;\n    int hp;\n};\n\nint main() {\n    Player p("Ada", 100);\n    p.hit(30);\n    std::cout << p.hp();   // 70\n}',
      js: 'class Player {\n  constructor(name, hp) {\n    this.name = name;\n    this.hp = hp;\n  }\n  hit(dmg) { this.hp -= dmg; }\n}\n\nconst p = new Player("Ada", 100);\np.hit(30);\nconsole.log(p.hp);   // 70',
    },
  },
  {
    id: "comments",
    en: "Comments",
    fa: "کامنت‌ها",
    code: {
      python: '# single line comment\n"""\nmulti-line string\n(often used as a comment)\n"""',
      c: '#include <stdio.h>\n\n/* multi-line\n   comment */\nint main(void) {\n    // single line comment (C99)\n    return 0;\n}',
      cpp: '/* multi-line comment */\nint main() {\n    // single line comment\n    return 0;\n}',
      js: '/* multi-line\n   comment */\nconsole.log("single line comment: //");',
    },
  },
];
