from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def debian_pkg(pkg_name: str, arch: bool = False) -> str:
    """
    通过 Debian QA 获取包版本信息

    Args:
        pkg_name: 包名字
        arch: 是否显示架构信息
    """
    async with ClientSession() as session:
        response = await session.get(
            "https://qa.debian.org/madison.php?package=" + pkg_name)
        text = await response.text()
        soup = BeautifulSoup(text, features="html.parser")
        selected = soup.select_one("#body > pre:nth-child(2)")
        if selected is None or len(selected.text) < 10:
            return "找不到这个包呢Σ( ° △ °|||)︴"
        result = selected.text
        if arch:
            return result
        return "\n".join(
            ['|'.join(l.split("|")[:-1]) for l in result.splitlines()])
