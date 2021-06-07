# JMdict_parser

The purpose of this project is to parse the Japanese-Multilingual Dictionary (JMdict) XML-file in order to produce a usable JSON file for use in other projects. Will eventually be used to analyze the JMdict file for various purposes.

The JMDict_e file included in this repo is the most recent version of the file as of 06/01/2021. Work will be done to ensure this project is compatible with future versions of the JMdict file, as features are occasionally added to the file.

## JMdict
[Information regarding the JMdict project can be found here](https://www.edrdg.org/jmdict/j_jmdict.html)

## Usage
```
git clone https://github.com/CameronChambers93/JMdict_parser.git
cd JMdict_parser
python3 JMDictToJSON.py [options]
```
Options
* --indent=number : Number of leading spaces added to each nested level when outputting JSON
* --low-memory: This mode allows the script to run on machines with low memory. When analytics are added to this project, it is likely that some may not function with this mode enabled

## Output
Current output is hardcoded to fit the needs of my own projects. Revisions will be made to make output format customizable. The following two examples show the format of the output. Note that since certain fields are optional for any given entry, some fields are omitted.


* indent=0
```
{ent_seq:"1004660",k_ele:[{keb:"この外",ke_pri:["spec1"]}],r_ele:[{reb:"このほか",re_pri:["spec1"]}],sense:[{pos:["conj"],misc:["uk"],gloss:["besides","moreover","in addition"]}]}
```
* indent=2
```
{
  ent_seq: "1004660",
  k_ele: [
    {
      keb: "この外",
      ke_pri: [
        "spec1"
      ]
    }
  ],
  r_ele: [
    {
      reb: "このほか",
      re_pri: [
        "spec1"
      ]
    }
  ],
  sense: [
    {
      pos: [
        "conj"
      ],
      misc: [
        "uk"
      ],
      gloss: [
        "besides",
        "moreover",
        "in addition"
      ]
    }
  ]
}
```