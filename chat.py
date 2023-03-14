#!/usr/bin/env python3
import openai
import sys
import cmd
import os
import json
from shutil import copyfile

openai_dir=os.path.expanduser("~/.config/openai")
if not os.path.exists(openai_dir):
    os.makedirs(openai_dir)

openai_config=os.path.expanduser("~/.config/openai.json")
if os.path.exists(openai_config):
    with open(openai_config, "rb") as f:
        config = json.loads(f.read())
        openai.api_key = config["token"]
else:
    print("%s not exist, please config as example" % openai_config)
    print('{"token": "you-api-token"}')
    sys.exit(-1)

class CLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "CHATGPT(default)> "
        self.model = "gpt-3.5-turbo"
        self.messages = []
        self.config = {}
        self.load("")
    

    def save(self, n):
        if n == "":
            self.prompt = "CHATGPT(default)> "
        else:
            self.prompt = "CHATGPT(%s)> " % n

    def load(self, n):
        self.save(n)
        self.history = os.path.join(openai_dir, "history%s.txt" % n)
        if os.path.exists(self.history):
            with open(self.history, "r") as f:
                for line in f:
                    self.messages.append(json.loads(line.strip()))
                
    def do_load(self, arg):
        self.load(arg)

    def do_ls(self, arg):
        historys = os.listdir(openai_dir)
        for h in historys:
            n = h.replace("history", "").replace(".txt", "")
            if n == "":
                print("default")
            else:
                print(n)

    def do_new(self, arg):
        self.save(arg)
        self.messages = []
        self.history = os.path.join(openai_dir, "history%s.txt" % arg)

    def do_clear(self, arg):
        self.messages = []

    def do_config(self, arg):
        if '=' in arg:
            k,v = arg.split('=')
            self.config[k] = v


    def do_token(self, arg):
        openai.api_key = arg

    def do_model(self, arg):
        self.model = arg

    def default(self, arg):
        self.do_ask(arg)

    def do_ask(self, arg):
        if 'no_history' in self.config and self.config['no_history'] == "1":
            self.messages = []
        self.messages.append({"role": "user", "content": arg})
        x = openai.ChatCompletion.create(
          model=self.model,
          messages=self.messages
        )
        print("answer:")
        for c in x["choices"]:
            ans = c["message"]["content"]
            self.messages.append({"role": "assistant", "content": ans})
            print(ans)

    def do_bye(self, arg):
        with open(self.history, "w") as f:
            for m in self.messages:
                f.write("%s\n" % json.dumps(m))
        return True

    def do_info(self, arg):
        print("model:%s" % self.model)
        print("history:")
        if self.config:
            for k,v in self.config.items():
                print("%s=%s" % (k,v))

        for m in self.messages:
            print(m)

    def help_version(self):
        print(
            "syntax: version [message]",
        )
        print("-- prints a version message")

if __name__ == '__main__':
    cli = CLI()
    cli.cmdloop()

