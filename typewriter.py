import utime
import uasyncio

# Typewriter effect should not pause the main thread, so we use uasyncio
# It should also return state like if it's done or not


class Typewriter:
    def __init__(self, textObject, timeline):
        self.textObject = textObject
        self.timeline = timeline

        self.total_time = 0

        for key in self.timeline:
            if isinstance(key, (int, float)):
                self.total_time += key
            else:
                self.total_time += len(key) * (1/30)

    def start(self):
        async def _start():
            for key in self.timeline:
                if isinstance(key, (int, float)):
                    await uasyncio.sleep(key)
                else:
                    await self._type(key)

        uasyncio.create_task(_start())

    async def _type(self, text):
        for char in text:
            self.textObject.text += char
            await uasyncio.sleep(1/30)
