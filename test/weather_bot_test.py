from unittest import TestCase, main

from plugin.weather import Weather


class WeatherBotTest(TestCase):
    def test_regex(self):
        bot = Weather()
        result = bot.resp_regex.findall(" 今天天气")
        self.assertEqual(result[0], ("", "今", ""))
        result = bot.resp_regex.findall(" 青岛今天天气")
        self.assertEqual(result[0], ("青岛", "今", ""))
        result = bot.resp_regex.findall("青岛今天天气如何")
        self.assertEqual(result[0], ("青岛", "今", "如何"))


if __name__ == "__main__":
    main()
