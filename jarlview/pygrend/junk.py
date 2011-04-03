    def pull_commands(self):
        #s = self.command_sock.recv(zmq.NOBLOCK)
        #print "waiting on command, before while"
        s = self.command_sock.recv()
        cmd = pickle.loads(s)
        print "got command, before while"
        #while ( s != None ): 
        while ( cmd.command != 'pas' ): 
            #cmd = pickle.loads(s)
            print "recv'd command: ", cmd.command
            if ( cmd.command == 'add' ):
                self.render_list.append(cmd.rect)
            elif ( cmd.command == 'upd' ):
                self.render_list[cmd.index] = cmd.rect
            elif ( cmd.command == 'del' ):
                del self.render_list[cmd.index]
            #s = self.command_sock.recv(zmq.NOBLOCK)
            print "waiting on command, in while"
            s = self.command_sock.recv()
            cmd = pickle.loads(s)
            print "got command, in while"

        if (self.dragging_rect > 0):
            r = self.hit_list[self.dragging_rect]
            r.x, r.y = event.pos
            c = pygrend.ZectCommand(cmd='upd', rect=r)
            cs = pickle.dumps(c)
            self.command_sock.send(cs)

        #self.hit_test()
        print "in mm, hit_index: ", self.dragging_rect
        #print "mouse at (%d, %d)" % event.pos

    
