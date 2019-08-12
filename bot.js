/**************************************************************************
                      ALANIS MORISSETTE DISCORD BOT
                      - Posts Alanis Morissette lyrics
                      - Calls Al gay
                      - Pings the hell out of Zerahl
                      - Sends thots and prayers
                      Written By: @Indoctrine#1337
                      Contributors: @Zerahl#6487
**************************************************************************/
const Discord = require('discord.js');
const auth = require('./auth.json');
const fs = require('fs');
const ironic = require('./ironic.json');
const bot = new Discord.Client();
const path = "/var/www/html/alanisbot/";
var hacktriggers;
var hackattempts = 0;
var hackdifficulty = 10;    // 0=guaranteed(1attempt) 1=testing(<10attempts) 5=easy(~25attempts) 10=normal(~35attempts) 20=hard(~50attempts) 40=TheGibson(~70attempts) (d100 is 50% chance with ~70 attempts)

function readFileSync(filePath) {
    var options = {encoding:'utf-8', flag:'r'};
    var buffer = fs.readFileSync(path + filePath, options);
    return buffer;
}

function writeFileSync(filePath, content, flag = 'w') {
    var options = {encoding:'utf-8', flag: flag};
    fs.writeFileSync(path + filePath, content, options);
}

bot.on('ready', () => {
  bot.user.setActivity('Ironic - Alanis Morissette', {type: 'LISTENING'});
  console.log('Connected as ' + bot.user.tag);
});

bot.on('message', (message) => {
  if(message.author != bot.user){
    if(message.content.match(/[i|l1]\s*r\s*[o0]\s*n\s*[yi|l1]/i)){
      var randomphrase = Math.floor(Math.random() * Math.floor(ironic.phrases.length));
      message.channel.send(ironic.phrases[randomphrase]);
    }

    else if(message.content.match(/(big gay)/i)){
      message.channel.send('<@268862954919821323> is the biggest of gays.');
    }

    else if(message.content.match(/(:<)/i)){
      hackattempts = readFileSync('db/hackattempts.txt');
      hackattempts++;
      writeFileSync('db/hackattempts.txt', hackattempts);

      var randompercentage = Math.floor(100 * Math.pow((Math.random()), (hackdifficulty/hackattempts)) + 1);
      if(randompercentage == 100){
        hacktriggers = readFileSync('db/hacktriggers.txt');
        hacktriggers++;
        writeFileSync('db/hacktriggers.txt', hacktriggers);
        console.log('Hack trigger number ' + hacktriggers + ' triggered in ' + hackattempts + ' tries.');
        message.channel.send('Attempt 0x' + hackattempts + ' successful. Hacking ' + randompercentage + '% complete. Consequences will never be the same, <@64909909052887040> has backtraced your IP and the cyberpolice are on their way.');
        hackattempts = 0;
        writeFileSync('db/hackattempts.txt', hackattempts);
      }

      else{
        message.channel.send('<@64909909052887040> is a big nerd. Hacking in progress, ' + randompercentage + '% complete.');
      }
    }

    else if(message.content.match(/(!hax)/i)){
      hacktriggers = readFileSync('db/hacktriggers.txt');
      message.channel.send('<@64909909052887040> has hacked the Gibson ' + hacktriggers + ' times. <:gotem:548663899466235915>');
    }

    else if(message.content.match(/(thot)/i)){
      message.react('🙏');
      message.channel.send('Sending thots and prayers to <@' + message.author.id + '>');
    }
  }
});

bot.login(auth.token);
bot.on('disconnect', function(errMsg, code) {
  bot.login(auth.token);
});
bot.on('error', function(console_error){
  writeFileSync('log/errors.log', '\n' + console_error, 'a');
  console.log(console_error);
  bot.login(auth.token);
});
