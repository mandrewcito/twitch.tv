using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;

namespace MonitorServidor.Hubs
{

    public class Stats
    {
        public double Cpu { get; set; }
        public double Ram { get; set; }
        public double Disk { get; set; }
    }
    public class MyHub : Hub
    {
        public async Task SendMessage(string user, Stats stats)
        {
            await Clients.All.SendAsync("ReceiveMessage", user, stats);
        }
    }
}