import pandas as pd
import numpy as np
from pygments.token import Token
import re
import sys
import pygments
import pygments.lexers

NAME_BREAKUP_RE = re.compile(r"[^a-zA-Z]+")

def extract_names(token):
	token = token.strip()
	prev_p = [""]

	def ret(name):
		r = name.lower()
		if len(name) >= 3:
			yield r
			if prev_p[0]:
				yield prev_p[0] + r
				prev_p[0] = ""
		else:
			prev_p[0] = r

	for part in NAME_BREAKUP_RE.split(token):
		if not part:
			continue
		prev = part[0]
		pos = 0
		for i in range(1, len(part)):
			this = part[i]
			if prev.islower() and this.isupper():
				yield from ret(part[pos:i])
				pos = i
			elif prev.isupper() and this.islower():
				if 0 < i - 1 - pos <= 3:
					yield from ret(part[pos:i - 1])
					pos = i - 1
				elif i - 1 > pos:
					yield from ret(part[pos:i])
					pos = i
			prev = this
		last = part[pos:]
		if last:
			yield from ret(last)

# Programming Languages that can be parsed by both linguist and pygments

common_langlist = ['ABAP',
 'ABNF',
 'AMPL',
 'ANTLR',
 'APL',
 'ActionScript',
 'Ada',
 'Agda',
 'Alloy',
 'ApacheConf',
 'AppleScript',
 'AspectJ',
 'Asymptote',
 'AutoHotkey',
 'AutoIt',
 'Awk',
 'Befunge',
 'BlitzBasic',
 'BlitzMax',
 'Boo',
 'Brainfuck',
 'Bro',
 'C',
 'CMake',
 'COBOL',
 'CSS',
 'Ceylon',
 'Chapel',
 'Cirru',
 'Clean',
 'Clojure',
 'CoffeeScript',
 'ColdFusion',
 'Coq',
 'Crystal',
 'Cuda',
 'Cython',
 'D',
 'Dart',
 'Diff',
 'Dylan',
 'EBNF',
 'ECL',
 'Eiffel',
 'Elixir',
 'Elm',
 'Erlang',
 'Factor',
 'Fancy',
 'Fantom',
 'Forth',
 'Fortran',
 'GAP',
 'Genshi',
 'Gherkin',
 'Gnuplot',
 'Go',
 'Golo',
 'Gosu',
 'Groovy',
 'HTML',
 'HTTP',
 'HXML',
 'Haml',
 'Handlebars',
 'Haskell',
 'Haxe',
 'Hy',
 'IDL',
 'INI',
 'Idris',
 'Io',
 'Ioke',
 'Isabelle',
 'J',
 'JSON',
 'JSONLD',
 'Jasmin',
 'Java',
 'JavaScript',
 'Julia',
 'Kotlin',
 'LLVM',
 'LSL',
 'Lasso',
 'Lean',
 'Limbo',
 'Liquid',
 'LiveScript',
 'Logos',
 'Logtalk',
 'Lua',
 'MATLAB',
 'Makefile',
 'Mako',
 'Markdown',
 'Mask',
 'Mathematica',
 'MiniD',
 'Modelica',
 'Monkey',
 'Moocode',
 'MoonScript',
 'Myghty',
 'NCL',
 'NSIS',
 'Nemerle',
 'NewLisp',
 'Nit',
 'Nix',
 'NumPy',
 'OCaml',
 'ObjDump',
 'Opa',
 'PHP',
 'PLpgSQL',
 'Pan',
 'Pawn',
 'Perl',
 'Pike',
 'PostScript',
 'PowerShell',
 'Prolog',
 'Pug',
 'Puppet',
 'Python',
 'QML',
 'REXX',
 'RHTML',
 'Racket',
 'Ragel',
 'Rebol',
 'Red',
 'Redcode',
 'RobotFramework',
 'Ruby',
 'Rust',
 'SAS',
 'SCSS',
 'SPARQL',
 'SQL',
 'Sass',
 'Scala',
 'Scaml',
 'Scheme',
 'Scilab',
 'Shen',
 'Slim',
 'Smali',
 'Smalltalk',
 'Smarty',
 'SourcePawn',
 'Stan',
 'Stata',
 'SuperCollider',
 'Swift',
 'SystemVerilog',
 'Tcl',
 'Tcsh',
 'TeX',
 'Text',
 'Thrift',
 'Turtle',
 'Twig',
 'TypeScript',
 'VCL',
 'VHDL',
 'Vala',
 'Verilog',
 'X10',
 'XML',
 'XQuery',
 'XSLT',
 'Xtend',
 'YAML',
 'Zephir',
 'eC',
 'mupad',
 'nesC',
 'ooc']

# Choose the corresponding pygment function according to linguist result

FileParseMap = {'ABAP': pygments.lexers.ABAPLexer,
 'APL': pygments.lexers.APLLexer,
 'ABNF': pygments.lexers.AbnfLexer,
 'ActionScript': pygments.lexers.ActionScriptLexer,
 'Ada': pygments.lexers.AdaLexer,
 'Agda': pygments.lexers.AgdaLexer,
 'Alloy': pygments.lexers.AlloyLexer,
 'AMPL': pygments.lexers.AmplLexer,
 'ANTLR': pygments.lexers.AntlrLexer,
 'ApacheConf': pygments.lexers.ApacheConfLexer,
 'AppleScript': pygments.lexers.AppleScriptLexer,
 'AspectJ': pygments.lexers.AspectJLexer,
 'Asymptote': pygments.lexers.AsymptoteLexer,
 'AutoIt': pygments.lexers.AutoItLexer,
 'AutoHotkey': pygments.lexers.AutohotkeyLexer,
 'Awk': pygments.lexers.AwkLexer,
 'Befunge': pygments.lexers.BefungeLexer,
 'BlitzBasic': pygments.lexers.BlitzBasicLexer,
 'BlitzMax': pygments.lexers.BlitzMaxLexer,
 'Boo': pygments.lexers.BooLexer,
 'Brainfuck': pygments.lexers.BrainfuckLexer,
 'Bro': pygments.lexers.BroLexer,
 'C': pygments.lexers.CLexer,
 'CMake': pygments.lexers.CMakeLexer,
 'COBOL': pygments.lexers.CobolLexer,
 'CSS': pygments.lexers.CssLexer,
 'Ceylon': pygments.lexers.CeylonLexer,
 'Chapel': pygments.lexers.ChapelLexer,
 'Cirru': pygments.lexers.CirruLexer,
 'Clean': pygments.lexers.CleanLexer,
 'Clojure': pygments.lexers.ClojureLexer,
 'CoffeeScript': pygments.lexers.CoffeeScriptLexer,
 'ColdFusion': pygments.lexers.ColdfusionLexer,
 'Coq': pygments.lexers.CoqLexer,
 'Crystal': pygments.lexers.CrystalLexer,
 'Cuda': pygments.lexers.CudaLexer,
 'Cython': pygments.lexers.CythonLexer,
 'D': pygments.lexers.DLexer,
 'Dart': pygments.lexers.DartLexer,
 'Diff': pygments.lexers.DiffLexer,
 'Dylan': pygments.lexers.DylanLexer,
 'EBNF': pygments.lexers.EbnfLexer,
 'ECL': pygments.lexers.ECLLexer,
 'Eiffel': pygments.lexers.EiffelLexer,
 'Elixir': pygments.lexers.ElixirLexer,
 'Elm': pygments.lexers.ElmLexer,
 'Erlang': pygments.lexers.ErlangLexer,
 'Factor': pygments.lexers.FactorLexer,
 'Fancy': pygments.lexers.FancyLexer,
 'Fantom': pygments.lexers.FantomLexer,
 'Forth': pygments.lexers.ForthLexer,
 'Fortran': pygments.lexers.FortranLexer,
 'GAP': pygments.lexers.GAPLexer,
 'Genshi': pygments.lexers.GenshiLexer,
 'Gherkin': pygments.lexers.GherkinLexer,
 'Gnuplot': pygments.lexers.GnuplotLexer,
 'Go': pygments.lexers.GoLexer,
 'Golo': pygments.lexers.GoloLexer,
 'Gosu': pygments.lexers.GosuLexer,
 'Groovy': pygments.lexers.GroovyLexer,
 'HTML': pygments.lexers.HtmlLexer,
 'HTTP': pygments.lexers.HttpLexer,
 'HXML': pygments.lexers.HxmlLexer,
 'Haml': pygments.lexers.HamlLexer,
 'Handlebars': pygments.lexers.HandlebarsLexer,
 'Haskell': pygments.lexers.HaskellLexer,
 'Haxe': pygments.lexers.HaxeLexer,
 'Hy': pygments.lexers.HyLexer,
 'IDL': pygments.lexers.IDLLexer,
 'INI': pygments.lexers.IniLexer,
 'Idris': pygments.lexers.IdrisLexer,
 'Io': pygments.lexers.IoLexer,
 'Ioke': pygments.lexers.IokeLexer,
 'Isabelle': pygments.lexers.IsabelleLexer,
 'J': pygments.lexers.JLexer,
 'JSON': pygments.lexers.JsonLexer,
 'JSONLD': pygments.lexers.JsonLdLexer,
 'Jasmin': pygments.lexers.JasminLexer,
 'Java': pygments.lexers.JavaLexer,
 'JavaScript': pygments.lexers.JavascriptLexer,
 'Julia': pygments.lexers.JuliaLexer,
 'Kotlin': pygments.lexers.KotlinLexer,
 'LLVM': pygments.lexers.LlvmLexer,
 'LSL': pygments.lexers.LSLLexer,
 'Lasso': pygments.lexers.LassoLexer,
 'Lean': pygments.lexers.LeanLexer,
 'Limbo': pygments.lexers.LimboLexer,
 'Liquid': pygments.lexers.LiquidLexer,
 'LiveScript': pygments.lexers.LiveScriptLexer,
 'Logos': pygments.lexers.LogosLexer,
 'Logtalk': pygments.lexers.LogtalkLexer,
 'Lua': pygments.lexers.LuaLexer,
 'MATLAB': pygments.lexers.MatlabLexer,
 'Makefile': pygments.lexers.MakefileLexer,
 'Mako': pygments.lexers.MakoLexer,
 'Markdown': pygments.lexers.MarkdownLexer,
 'Mask': pygments.lexers.MaskLexer,
 'Mathematica': pygments.lexers.MathematicaLexer,
 'MiniD': pygments.lexers.MiniDLexer,
 'Modelica': pygments.lexers.ModelicaLexer,
 'Monkey': pygments.lexers.MonkeyLexer,
 'Moocode': pygments.lexers.MOOCodeLexer,
 'MoonScript': pygments.lexers.MoonScriptLexer,
 'Myghty': pygments.lexers.MyghtyLexer,
 'NCL': pygments.lexers.NCLLexer,
 'NSIS': pygments.lexers.NSISLexer,
 'Nemerle': pygments.lexers.NemerleLexer,
 'NewLisp': pygments.lexers.NewLispLexer,
 'Nit': pygments.lexers.NitLexer,
 'Nix': pygments.lexers.NixLexer,
 'NumPy': pygments.lexers.NumPyLexer,
 'OCaml': pygments.lexers.OcamlLexer,
 'ObjDump': pygments.lexers.ObjdumpLexer,
 'Opa': pygments.lexers.OpaLexer,
 'PHP': pygments.lexers.PhpLexer,
 'PLpgSQL': pygments.lexers.PlPgsqlLexer,
 'Pan': pygments.lexers.PanLexer,
 'Pawn': pygments.lexers.PawnLexer,
 'Perl': pygments.lexers.PerlLexer,
 'Pike': pygments.lexers.PikeLexer,
 'PostScript': pygments.lexers.PostScriptLexer,
 'PowerShell': pygments.lexers.PowerShellLexer,
 'Prolog': pygments.lexers.PrologLexer,
 'Pug': pygments.lexers.PugLexer,
 'Puppet': pygments.lexers.PuppetLexer,
 'Python': pygments.lexers.PythonLexer,
 'QML': pygments.lexers.QmlLexer,
 'REXX': pygments.lexers.RexxLexer,
 'RHTML': pygments.lexers.RhtmlLexer,
 'Racket': pygments.lexers.RacketLexer,
 'Ragel': pygments.lexers.RagelLexer,
 'Rebol': pygments.lexers.RebolLexer,
 'Red': pygments.lexers.RedLexer,
 'Redcode': pygments.lexers.RedcodeLexer,
 'RobotFramework': pygments.lexers.RobotFrameworkLexer,
 'Ruby': pygments.lexers.RubyLexer,
 'Rust': pygments.lexers.RustLexer,
 'SAS': pygments.lexers.SASLexer,
 'SCSS': pygments.lexers.ScssLexer,
 'SPARQL': pygments.lexers.SparqlLexer,
 'SQL': pygments.lexers.SqlLexer,
 'Sass': pygments.lexers.SassLexer,
 'Scala': pygments.lexers.ScalaLexer,
 'Scaml': pygments.lexers.ScamlLexer,
 'Scheme': pygments.lexers.SchemeLexer,
 'Scilab': pygments.lexers.ScilabLexer,
 'Shen': pygments.lexers.ShenLexer,
 'Slim': pygments.lexers.SlimLexer,
 'Smali': pygments.lexers.SmaliLexer,
 'Smalltalk': pygments.lexers.SmalltalkLexer,
 'Smarty': pygments.lexers.SmartyLexer,
 'SourcePawn': pygments.lexers.SourcePawnLexer,
 'Stan': pygments.lexers.StanLexer,
 'Stata': pygments.lexers.StataLexer,
 'SuperCollider': pygments.lexers.SuperColliderLexer,
 'Swift': pygments.lexers.SwiftLexer,
 'SystemVerilog': pygments.lexers.SystemVerilogLexer,
 'Tcl': pygments.lexers.TclLexer,
 'Tcsh': pygments.lexers.TcshLexer,
 'TeX': pygments.lexers.TexLexer,
 'Text': pygments.lexers.TextLexer,
 'Thrift': pygments.lexers.ThriftLexer,
 'Turtle': pygments.lexers.TurtleLexer,
 'Twig': pygments.lexers.TwigLexer,
 'TypeScript': pygments.lexers.TypeScriptLexer,
 'VCL': pygments.lexers.VCLLexer,
 'VHDL': pygments.lexers.VhdlLexer,
 'Vala': pygments.lexers.ValaLexer,
 'Verilog': pygments.lexers.VerilogLexer,
 'X10': pygments.lexers.X10Lexer,
 'XML': pygments.lexers.XmlLexer,
 'XQuery': pygments.lexers.XQueryLexer,
 'XSLT': pygments.lexers.XsltLexer,
 'Xtend': pygments.lexers.XtendLexer,
 'YAML': pygments.lexers.YamlLexer,
 'Zephir': pygments.lexers.ZephirLexer,
 'eC': pygments.lexers.ECLexer,
 'mupad': pygments.lexers.MuPADLexer,
 'nesC': pygments.lexers.NesCLexer,
 'ooc': pygments.lexers.OocLexer}

## --------------------------------------------------------

user = sys.argv[1]
repo = sys.argv[2]
#token_name = user + '_' + repo + '_token_name'
#with open(token_name, 'r') as f:
#	source_code = f.readlines()
#	identifiers = [re.split("\t|\n|'", tn)[2] for tn in source_code]
linguist = str(repo) + "/linguistfiles.log"
linguistfiles = pd.read_csv(linguist, sep=';', header=None, names=['Language', 'path'])
linguistfiles = linguistfiles[linguistfiles['Language'].isin(common_langlist)]

token = []
for lang, files in linguistfiles.groupby('Language'):
    print(lang)
    for path in files['path']:
        filename = repo + '/' + path
        with open(filename, 'r', encoding="utf8", errors='ignore') as f:
            code = f.read()
        token.extend(list(pygments.lex(code, FileParseMap[lang]())))

# Extract only Token.Name*

token_name = list(filter(lambda x: 'Token.Name' in str(x[0]), token)) 

# Get rid of Token.Name.Attribute, Token.Name.Tag and Token.Name.Entity

token_name = list(filter(lambda x: str(x[0]) not in ['Token.Name.Attribute', 'Token.Name.Tag', 'Token.Name.Entity'], token_name))  

identifiers = [x[1] for x in token_name]

splitted_identifiers = [" "]
for identifier in identifiers:
	splitted_identifiers.extend(list(extract_names(identifier)))
splitted_identifiers.remove(' ')
# Extract Token.Comment

token_comment = list(filter(lambda x: 'Token.Comment' in str(x[0]), token)) 
comment = [x[1] for x in token_comment]

splitted_comment = [" "]
for identifier in comment:
	splitted_comment.extend(list(extract_names(identifier)))
splitted_comment.remove(' ')

identifier_result = " ".join(splitted_identifiers)
comment_result = " ".join(splitted_comment)

with open("source_code_identifier_names", 'a') as s:
	s.write(user + '/' + repo + '\t' + identifier_result + '\t' + comment_result + '\n')



