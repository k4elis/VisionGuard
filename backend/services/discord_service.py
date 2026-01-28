"""
Discord bot service for sending notifications
"""
import discord
from discord.ext import commands
import asyncio
from typing import Optional
import os

from backend.core.config import settings


class DiscordNotifier:
    """Discord notification service"""
    
    def __init__(self):
        self.token = settings.DISCORD_BOT_TOKEN
        self.channel_id = settings.DISCORD_CHANNEL_ID
        self.client = None
        self.channel = None
        self.ready = False
        
    async def initialize(self):
        """Initialize Discord bot"""
        if not self.token or not self.channel_id:
            print("Discord bot token or channel ID not configured")
            return
        
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        
        @self.client.event
        async def on_ready():
            print(f'Discord bot logged in as {self.client.user}')
            self.channel = self.client.get_channel(int(self.channel_id))
            self.ready = True
        
        # Start bot in background
        asyncio.create_task(self.client.start(self.token))
        
        # Wait for bot to be ready
        for _ in range(30):  # Wait up to 30 seconds
            if self.ready:
                break
            await asyncio.sleep(1)
    
    async def send_motion_alert(self, camera_id: int, confidence: float, 
                               screenshot_path: Optional[str] = None,
                               recording_path: Optional[str] = None):
        """Send motion detection alert to Discord"""
        if not self.ready or not self.channel:
            print("Discord bot not ready")
            return
        
        # Create embed message
        embed = discord.Embed(
            title=f"🚨 Motion Detected on Camera {camera_id}",
            description=f"Motion detected with {confidence*100:.1f}% confidence",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Camera", value=f"Camera {camera_id}", inline=True)
        embed.add_field(name="Confidence", value=f"{confidence*100:.1f}%", inline=True)
        
        # Attach screenshot if available
        files = []
        if screenshot_path and os.path.exists(screenshot_path):
            files.append(discord.File(screenshot_path, filename="screenshot.jpg"))
            embed.set_image(url="attachment://screenshot.jpg")
        
        try:
            await self.channel.send(embed=embed, files=files)
        except Exception as e:
            print(f"Error sending Discord notification: {e}")
    
    async def close(self):
        """Close Discord connection"""
        if self.client:
            await self.client.close()


# Global Discord notifier instance
discord_notifier = None


async def get_discord_notifier() -> DiscordNotifier:
    """Get or create Discord notifier instance"""
    global discord_notifier
    if discord_notifier is None:
        discord_notifier = DiscordNotifier()
        await discord_notifier.initialize()
    return discord_notifier
