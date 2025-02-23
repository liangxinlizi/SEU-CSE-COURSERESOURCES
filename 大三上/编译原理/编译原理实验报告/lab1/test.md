
| **Token Type**   | **Example**          | **Regular Expression**               |
| --- | --- | --- |
| `keyword`        | `main`              | `main/if/while/else/return/for/break/continue/do/switch/void/int/float/char/const`                               |
| `id`| Custom Identifier   | `[a-zA-Z_][a-zA-Z0-9_]*`             |
| `num`            | Integer Constant    | `[0-9]+`                             |
| `float`          | Floating Constant   | `[0-9]+\.[0-9]+`                     |
| `string`         | String Constant     | `"[^"]*"`                            |
| `operator`       | `=`                 | `=`                                  |
| `error`          | Unknown Symbol      | `.` (Matches any single symbol not conforming to the above rules) |

--------------------------------------------------

| Lexical Unit Type | Lexical Unit Example | Number |
| --- | --- | --- |
| `keyword` | `main` | 1 |
| `keyword` | `int` | 2 |
| `keyword` | `char` | 3 |
| `keyword` | `if` | 4 |
| `keyword` | `else` | 5 |
| `keyword` | `for` | 6 |
| `keyword` | `while` | 7 |
| `keyword` | `return` | 8 |
| `keyword` | `void` | 9 |
| `keyword` | `float` | 10 |
| `keyword` | `then` | 11 |
| `keyword` | `switch` | 12 |
| `keyword` | `break` | 13 |
| `keyword` | `continue` | 14 |
| `keyword` | `do` | 15 |
| `keyword` | `const` | 16 |
| `id` | Custom identifier | Numbered starting from 1 according to the insertion order in `flag_table` (determined by `flag_table.size() + 1` in the code) |
| `num` | Integer constant | Numbered starting from 1 according to the insertion order in `num_table` (determined by `num_table.size() + 1` in the code, and the category number is assumed to be 20) |
| `float` | Floating-point constant | Numbered starting from 1 according to the insertion order in `num_table` (determined by `num_table.size() + 1` in the code, and the category number is assumed to be 30) |
| `string` | String constant | Numbered starting from 1 according to the insertion order in `str_table` (determined by `str_table.size() + 1` in the code, and the category number is 50) |
| `operator` | `=` | 21 |
| `operator` | `+` | 22 |
| `operator` | `-` | 23 |
| `operator` | `*` | 24 |
| `operator` | `/` | 25 |
| `operator` | `(` | 26 |
| `operator` | `)` | 27 |
| `operator` | `[` | 28 |
| `operator` | `]` | 29 |
| `operator` | `{` | 30 |
| `operator` | `}` | 31 |
| `operator` | `,` | 32 |
| `operator` | `:` | 33 |
| `operator` | `;` | 34 |
| `operator` | `>` | 35 |
| `operator` | `<` | 36 |
| `operator` | `>=` | 37 |
| `operator` | `<=` | 38 |
| `operator` | `==` | 39 |
| `operator` | `"` | 40 |
| `error` | (Various unknown symbols that do not conform to the above rules) | No fixed number |