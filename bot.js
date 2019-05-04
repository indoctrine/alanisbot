var Discord = require('discord.io');
var auth = require('./auth.json');
var fs = require('fs');
var ironic = require('./ironic.json');

function readFileSync(filePath){
    var options = {encoding:'utf-8', flag:'r'};
    var buffer = fs.readFileSync(filePath, options);
    return buffer;
}

function writeFileSync(filePath, content) {
    var options = {encoding:'utf-8', flag:'w'};
    fs.writeFileSync(filePath, content, options);
}

var hacktriggers;

// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});

bot.on('ready', () => {
  bot.setPresence({
    status: 'online',
    game: {
      name: 'Ironic - Alanis Morissette',
      type: 2,
      url: 'https://open.spotify.com/track/1d6KS9GH06JAd19uiBy9IE?si=yM8Fg9XyTt2oX7bVq0LK6g'
    }
  });
});

bot.on('message', function (user, userID, channelID, message, evt) {
  if(userID != bot.id){
    if(message.match(/[i|l1]\s*r\s*[o0]\s*n\s*[yi|l1]/i)){
      var randomphrase = Math.floor(Math.random() * Math.floor(ironic.phrases.length));
      bot.sendMessage({
        to: channelID,
        message: ironic.phrases[randomphrase]
      });
    }
   else if(message.match(/(big gay)/i)){
  	bot.sendMessage({
  	 to: channelID,
  	 message: "<@268862954919821323> is the biggest of gays."
  	});
   }

   else if(message.match(/(:<)/i)){
     var randompercentage = Math.floor((Math.random() * 100) + 1);
     if(randompercentage == 100){
       hacktriggers = readFileSync('hacktriggers.txt');
       hacktriggers++;
       writeFileSync('hacktriggers.txt', hacktriggers);

       bot.sendMessage({
       	 to: channelID,
       	 message: "Hacking " + randompercentage + "% complete. Consequences will never be the same, <@64909909052887040> has backtraced your IP and the cyberpolice are on their way."
     	});
     }
	   else{
       bot.sendMessage({
      	 to: channelID,
      	 message: "<@64909909052887040> is a big nerd. Hacking in progress, " + randompercentage + "% complete."
    	});
    }
  }

  else if(message.match(/(!hax)/i)){
    hacktriggers = readFileSync('hacktriggers.txt');
    bot.sendMessage({
      to: channelID,
      message: "<@64909909052887040> has hacked the Gibson " + hacktriggers + " times. <:gotem:548663899466235915>"
    })
  }
  else if(message.match(/(thot)/i)){
    bot.sendMessage({
      to: channelID,
      message: "Sending thots and prayers to <@" + userID + "> :pray:"
    })
  }
  }
});
bot.on('disconnect', function(errMsg, code) {
  bot.connect();
});
