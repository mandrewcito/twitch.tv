using System.Threading.Channels;
using Microsoft.AspNetCore.SignalR;
using System.Threading.Tasks;
using System.Threading;
using System;

namespace streamming
{
    public class StreamHub : Hub
    {
        public ChannelReader<int> Counter(
            int count,
            int delay)
        {
            var channel = Channel.CreateUnbounded<int>();

            _ = WriteItemsAsync(channel.Writer, count, delay);

            return channel.Reader;
        }

        private async Task WriteItemsAsync(
            ChannelWriter<int> writer,
            int count,
            int delay)
        {
            Exception localException = null;
            try
            {
                for (var i = 0; i < count; i++)
                {
                    await writer.WriteAsync(i);
                    await Task.Delay(delay);
                }
            }
            catch (Exception ex)
            {
                localException = ex;
            }

            writer.Complete(localException);
        }
        public async Task SendMessage(string user, string message)
        {
            await Clients.All.SendAsync("ReceiveMessage", user, message);
        }
    }
}