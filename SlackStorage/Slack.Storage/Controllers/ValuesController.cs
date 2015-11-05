using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.AspNet.Mvc;
using Newtonsoft.Json;

namespace Slack.Storage.Controllers
{
    public class Message
    {
        public Message(string content)
        {
            Content = content;
            Created = DateTime.UtcNow;
        }

        public DateTime Created { get; set; }
        public string Content { get; set; }
    }

    public class HookPayload
    {
        public string Created { get; set; }
        public string Text { get; set; }
    }

    [Route("api/message")]
    public class ValuesController : Controller
    {
        private static readonly List<Message> Messages = new List<Message>();

        [HttpGet]
        public List<Message> Get()
        {
            var messageCopy = Messages.ToList();
            Messages.Clear();
            return messageCopy;
        }

        [HttpPost]
        public void Post([FromBody] HookPayload slackMessage)
        {
            if (Request.Body.CanSeek)
                Request.Body.Position = 0;

            var input = new StreamReader(Request.Body).ReadToEnd();

            var queryDictionary = Microsoft.AspNet.WebUtilities.QueryHelpers.ParseQuery(input);

            Messages.Add(new Message(queryDictionary["text"].Aggregate("", (a,b) => a+b).Replace("!say","")));

            /*
            var regex = new Regex(".*text=(.*?)&.*");

            if (regex.IsMatch(input))
            {
                Messages.Add(new Message(regex.Match(input).Groups[1].Value));
            }
            else
            {
                Messages.Add(new Message("EI LÖYTYNYT: " + input));
            }*/
        }
    }
}
