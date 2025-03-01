<h1 align="center">
  ZhiXueHacker
</h1>
<p align="center">
  智学网桌面端实用工具。
</p>

<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/v/tag/HShiDianLu/ZhiXueHacker?label=Version&color=vue" alt="Version"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/HShiDianLu/ZhiXueHacker/total?label=Downloads&color=vue " alt="Downloads"/>
  </a>
  
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Windows-Vue" alt="Platform">
  </a>
  
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Lisence-MIT-Vue" alt="Downloads"/>
  </a>
  
  <br>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Language-Python-blue" alt="Shitcode"/>
  </a>
</p>

## 功能
- 试卷信息查看
- 考试排名
- 答题卡下载
- 得分详情
- 试卷下载
- 在线考试

## 注意
**源代码不包含Pandoc，若要下载试卷请将Pandoc置于工作目录内。**

**试卷必须入库才能下载。**

用户名和密码是保存在本地的。

如果登录时WebEngineView经常闪退，请将设置-高级-登录方式改为Selenium。

Copyright © 2024-2025 by HShiDianLu.

---

## Pandoc License
Pandoc
Copyright (C) 2006-2023 John MacFarlane <jgm at berkeley dot edu>

With the exceptions noted below, this code is released under the [GPL],
version 2 or later:

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

The GNU General Public License is available in the file COPYING.md in
the source distribution.  On Debian systems, the complete text of the
GPL can be found in `/usr/share/common-licenses/GPL`.

[GPL]: https://www.gnu.org/copyleft/gpl.html

Pandoc's complete source code is available from the [Pandoc home page].

[Pandoc home page]: https://pandoc.org

Pandoc includes some code with different copyrights, or subject to different
licenses.  The copyright and license statements for these sources are included
below.  All are GPL-compatible licenses.

----------------------------------------------------------------------
The modules in the `pandoc-types` repository (Text.Pandoc.Definition,
Text.Pandoc.Builder, Text.Pandoc.Generics, Text.Pandoc.JSON,
Text.Pandoc.Walk) are licensed under the BSD 3-clause license:

Copyright (c) 2006-2023, John MacFarlane

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * Neither the name of John MacFarlane nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

----------------------------------------------------------------------
Pandoc's templates (in `data/templates`) are dual-licensed as either
GPL (v2 or higher, same as pandoc) or (at your option) the BSD
3-clause license.

Copyright (c) 2014--2023, John MacFarlane

----------------------------------------------------------------------
src/Text/Pandoc/Writers/Muse.hs
Copyright (C) 2017-2020 Alexander Krotov

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Writers/Texinfo.hs
Copyright (C) 2008-2023 John MacFarlane and Peter Wang

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Writers/OpenDocument.hs
Copyright (C) 2008-2023 Andrea Rossato and John MacFarlane

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Writers/Org.hs
Copyright (C) 2010-2023 Puneeth Chaganti, John MacFarlane, and
                        Albert Krewinkel

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Writers/ZimWiki.hs
Copyright (C) 2017 Alex Ivkin

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/Docx.hs
src/Text/Pandoc/Readers/Docx/*
Copyright (C) 2014-2020 Jesse Rosenthal

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/Textile.hs
Copyright (C) 2010-2023 Paul Rivier and John MacFarlane

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/TikiWiki.hs
Copyright (C) 2017 Robin Lee Powell

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/JATS.hs
Copyright (C) 2017-2018 Hamish Mackenzie

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/EPUB.hs
Copyright (C) 2014-2023 Matthew Pickering and John MacFarlane

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/Org.hs
src/Text/Pandoc/Readers/Org/*
test/Tests/Readers/Org/*
Copyright (C) 2014-2023 Albert Krewinkel

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
pandoc-lua-engine/src/Text/Pandoc/Lua.hs
pandoc-lua-engine/src/Text/Pandoc/Lua/*
pandoc-lua-engine/test/lua/*
Copyright (C) 2017--2023 Albert Krewinkel and John MacFarlane

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/Jira.hs
src/Text/Pandoc/Writers/Jira.hs
test/Tests/Readers/Jira.hs
Copyright (C) 2019--2023 Albert Krewinkel

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/FB2.hs
Copyright (C) 2018--2019 Alexander Krotov

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
The dzslides template contains JavaScript and CSS from Paul Rouget's
dzslides template.
https://github.com/paulrouget/dzslides

Released under the Do What the Fuck You Want To Public License.

------------------------------------------------------------------------
Pandoc embeds a Lua interpreter (via hslua).

Copyright © 1994–2022 Lua.org, PUC-Rio.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
