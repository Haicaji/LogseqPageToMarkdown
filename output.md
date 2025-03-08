
- 进入题目网站, 直接给了 `index.php` 的源码
# 一段段分析源码

- `include("get_flag.php")`
	- 使 `get_flag.php` 的源码[包含]([[文件包含漏洞]])进index.php中, 并且执行
- 随后 `global $flag;`, 定义了一个全局变量 `flag`
	- 这个变量的值可能就是需要的Flag
	- 这里注意的是, 虽然 `get_flag.php` 的包含语句在 `global $flag;`之前, 但是其的执行顺序其实在整个文件之后, 所以 `get_flag.php` 可以对 `global $flag;` 进行赋值
- `session_start();`
	- 开启 [SESSION]([[Session]])
- 然后就是 `hello_ctf`, `get_fun`, `start` 三个函数, 先不看它们
- 接着就是 `isset($_GET['action']) ? start($_GET['action']) : '';`
	- 这其实是 `if else` 的简写, 即使用了3元运算符
	- `isset($_GET['action'])` 是条件
		- 是否GET是否传递了`action`这个参数
	- 问号后面是当条件为真时, 执行的语句
		- 即`start($_GET['action'])`
		- 调用 `start` 这个函数, 并把 GET 传入的参数 `action` 作为函数的参数
	- 冒号后面是当条件为假时, 执行的语句
		- 即 ''
		- 就是给出一个空字符串
		- 什么也不做
- 最后是 `highlight_file(__FILE__);`
	- 这段代码使这个 php 的代码显示出来
- 那接着把重点放在 即`start($_GET['action'])`
	- 进入 `start` 这个函数
		- 首先执行了 `get_fun` 这个函数, 并把函数的返回值赋予给 `random_func` 这个变量
		- 进入 `get_fun` 这个函数进行分析
			- 有个字符串数组 `func_list`
			- 然后判断 [SESSION]([[Session]]) 中有没有 `random_func` 这个字段
			- 没有的话执行这个语句 `$_SESSION['random_func'] = $func_list[array_rand($func_list)];`
				- 主要看 `array_rand($func_list)`, 它的意思是随机返回一个 `func_list` 这个数组的一个键值(即索引)
				- 总结来说就是把 `func_list` 随机一个成员赋值给 SESSION的 `random_func` 字段
			- 然后就是 `$url_fucn = preg_replace('/_/', '-', $_SESSION['random_func']);` 这个语句
				- 重点看  `preg_replace('/_/', '-', $_SESSION['random_func']);` 函数
					- 第一个参数 `'/_/'` 这是正则表达式, 表示要检索的字符串
						- `/` 是正则表达式的分隔符,  常用 `/`，也可以用 `~ #`  等
						- `_` 表示要匹配的字面字符下划线
					- 第二个参数  ' -'  表示要替换为的目标字符串
					- 第三个参数 `$_SESSION['random_func']`, 即被操作的字符串
					- 整个函数意思就是
						- 把 `$_SESSION['random_func']` 字符串的 `_` 替换为 `-`
				- 最后将 `preg_replace` 替换后的 `$_SESSION['random_func']` 赋值给 `url_fucn` 变量
				- 而其实这个操作, 只是为了方便下文输出 php 文档相关函数的url, 对 `get_fun` 函数的返回值没有影响
			- 而 `get_fun` 函数最后返回 `$_SESSION['random_func']` 的值
		- `random_func` 得到 `get_fun` 函数的返回值(即`func_list`数组中随机一个函数方法)
		- 然后就是判断传入的参数 `act` (即GET请求传入的action参数) 是不是 `r`
			- 是的话, 就执行 `session_unset()`, `session_destroy()`
			- 即清除当前 Session 的所有字段和删除当前Session对话
		- 然后接着就是判断 `act` 是不是 `submit`
			- 如果是的话, 就是把 POST 请求的 `content` 参数交给 `user_content` 变量
			- 然后执行 `hello_ctf` 函数, 并把 `random_func`, `user_content` 两个变量作为参数传递进去
	- 接着进入 `hello_ctf` 函数
		- 首先把全局变量 `flag` 声明进这个函数中, 使这个函数调用的 `flag` 变量为全局变量 `flag`
		- 然后对传进的参数 `function`(即 `get_fun()` 函数随机选择的函数) 和 `contect`(即 POST 请求的内容) 进行拼接字符串
			- 然后把拼接后的值传递给 `code` 变量
			- 如 `function` 为 `eval`, `contect` 为 `"ls"`
				- 那么 `code` 就是 `eval("ls");`
		- 然后输出 `code` 变量
		- 并且使用 `eval($code);` 执行 `code` 变量中的代码
- 整个代码就这么讲完了, 总结一下就是
	- GET 请求中, 通过调节`action`的值, 是否等于 `r`, 可以刷新 Session 中的 `random_func` 的值, 然后如果`action`的值等于 `submit` 时, 就用 `random_func` 中的函数, 以 POST 请求中的 `content` 参数作为参数, 被 `eval()` 执行
- 并且整个代码看下来, 似乎全局变量 `$flag` 就是我们需要获取的, 那我们的目的就是通过 GET 请求拿到我们想要的 `random_func`, 然后参数构造 POST 请求传入 `content`, 从而输出全局变量 `$flag`
# 最后解题步骤如下

- 首先使用 BurpSuite 随便抓一个包, `Ctrl+R`->使报文发送到重放器, 记得发两份, 然后进入[重放器(Repeater)]([[BurpSuite-Repeater]])
- 第一份使用GET请求
	- 添加 GET 参数 `action=r`
	- ![image.png](../assets/image_1741275879119_0.png){:height 393, :width 360}
- 第二份使用 POST 请求
	- 右键报文->修改请求方式
	- 此时, 原本的 GET 请求的参数会被移到底下来, 但是对于题目而言, 它依然是要为 GET 请求传入, 把它移到原来位置去, 即添加 GET 参数 `action=submit`
	- 然后添加 POST 参数 `content="echo $flag"`
	- ![image.png](../assets/image_1741276139814_0.png){:height 448, :width 380}
- 然后轮流发送这两份报文, 追后就可以使 `random_func` 为 `assert`, 然后让 `eval`执行 `assert("echo $flag");` , 得到 flag
	- ![image.png](../assets/image_1741276402609_0.png){:height 651, :width 330}
- ~~这个解题步骤是基于只会一种方法的情况下~~
# 可能到这还会有些问题

- 为什么是两份报文轮流发, 按照 整个代码就这么讲完了, 总结一下就是 的不是只要通过 `action=r` 调整 Session 中的函数为 `assert`, 然后再发 `action=sbumit` 报文就可以了吗?
	- 其实这是对整个PHP代码逻辑的误解
	- `action=r` 时, 虽然会刷新 Session, 但是是在最末尾进行刷新, 也就是在这个报文之后, 已经不存在 Session
	- 而只有当 `action=submit` 时才可以获取 Session, 但是这个报文又不会删除不要的 Session
	- 所有就要两个一起配合
- 为什么会选择 `assert` 函数, 而不是其他的
	- 因为刚好这个会 🫠(请在学习中, 每种方法都去尝试)
	- 这里的函数其实都可以用来获取 flag
	- 具体示例如下(来自靶场官方WP)
		| 函数 | 说明 | 示例代码 |
		|---|---|---|
		| `${}` | 用于复杂的变量解析，通常在字符串内用来解析变量或表达式。可以配合 `eval` 或其他动态执行代码的功能，用于间接执行代码。 | `eval('${flag}');` |
		| [`eval()`](https://www.php.net/manual/zh/function.eval.php) | 用于执行一个字符串作为 PHP 代码。可以执行任何有效的 PHP 代码片段。没有返回值，除非在执行的代码中明确返回。 | `eval('echo $flag;');` |
		| [`assert()`](https://www.php.net/manual/zh/function.assert.php) | 测试表达式是否为真。PHP 8.0.0 之前，如果 `assertion` 是字符串，将解释为 PHP 代码并通过 `eval()` 执行。**PHP 8.0.0 后移除该功能。** | `assert(print_r($flag));` |
		| [`call_user_func()`](https://www.php.net/manual/zh/function.call-user-func.php) | 用于调用回调函数，可以传递多个参数给回调函数，返回回调函数的返回值。适用于动态函数调用。 | `call_user_func('print_r', $flag);` |
		| [`create_function()`](https://www.php.net/manual/zh/function.create-function.php) | 创建匿名函数，接受两个字符串参数：参数列表和函数体。返回一个匿名函数的引用。**自 PHP 7.2.0 起被_废弃_，并自 PHP 8.0.0 起被_移除_。** | `create_function('$a', 'echo $flag;')($a);` |
		| [`array_map()`](https://www.php.net/manual/zh/function.array-map.php) | 将回调函数应用于数组的每个元素，返回一个新数组。适用于转换或处理数组元素。 | `array_map(print_r($flag), $a);` |
		| [`call_user_func_array()`](https://www.php.net/manual/zh/function.call-user-func-array.php) | 调用回调函数，并将参数作为数组传递。适用于动态参数数量的函数调用。 | `call_user_func_array(print_r($flag), array());` |
		| [`usort()`](https://www.php.net/manual/zh/function.usort.php) | 对数组进行自定义排序，接受数组和比较函数作为参数。适用于根据用户定义的规则排序数组元素。 | `usort($a,print_r($flag));` |
		| [`array_filter()`](https://www.php.net/manual/zh/function.array-filter.php) | 过滤数组元素，如果提供回调函数，仅包含回调返回真值的元素；否则，移除所有等同于false的元素。适用于基于条件移除数组中的元素。 | `array_filter($a,print_r($flag));` |
		| [`array_reduce()`](https://www.php.net/manual/zh/function.array-reduce.php) | 迭代一个数组，通过回调函数将数组的元素逐一减少到单一值。接受数组、回调函数和可选的初始值。 | `array_reduce($a,print_r($flag));` |
		| [`preg_replace()`](https://www.php.net/manual/zh/function.preg-replace.php) | 执行正则表达式的搜索和替换。可以是单个字符串或数组。适用于基于模式匹配修改文本内容。**依赖 /e 模式，该模式自 PHP7.3 起被取消。** | `preg_replace('/(.*)/ei', 'strtolower("\\1")', ${print_r($flag)});` |
		| [`ob_start()`](https://www.php.net/manual/zh/function.ob-start.php) | ob_start — 打开输出控制缓冲,可选回调函数作为参数来处理缓冲区内容。 | `ob_start(print_r($flag));` |
