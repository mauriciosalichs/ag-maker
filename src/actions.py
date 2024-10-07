class Actions:
    def __init__(self, game, actions_data):
        self.game = game
        self.checkpoints = set(actions_data['checkpoints'])
        self.grabRules = actions_data['grabRules']
        self.useRules = actions_data['useRules']
        self.useWithTargetRules = actions_data['useWithTargetRules']
        self.triggers = actions_data['triggers']

    def allowGrab(self, obj_id):
        print("allowGrab", obj_id)
        object_has_rules = False
        for obj,cpCond,response in self.grabRules:
            if obj == obj_id:
                object_has_rules = True
                if all(elem in self.checkpoints for elem in cpCond):
                    if response == 'ok':
                        return True
                    else:
                        self.launch_trigger(response)
        return not object_has_rules

    def allowUse(self, obj_id):
        print("allowUse",obj_id)
        for obj, cpCond, response in self.useRules:
            if obj == obj_id:
                if all(elem in self.checkpoints for elem in cpCond):
                    self.checkpoints.add(response)
                    self.launch_trigger(response)
                    return True
        return False

    def allowUseWithTarget(self, target_id, obj_id):
        print("allowUseWithTarget",obj_id,target_id)
        for obj, target, cpCond, response in self.useWithTargetRules:
            if obj == obj_id and target == target_id:
                if all(elem in self.checkpoints for elem in cpCond):
                    if response.startswith('nu'):
                        self.game.show_text(response[2:])
                    else:
                        self.checkpoints.add(response)
                        self.launch_trigger(response)
                    return True
        return False

    def allowSpeak(self, char_id):
        pass

    def launch_trigger(self, cpId):
        triggers = self.triggers[cpId]
        for tTarget, tParam, tValue in triggers:
            print("LAUNCHING", tTarget, tParam, tValue)
            entity = self.get_entity(tTarget)
            attr = getattr(entity, tParam)
            attr(tValue)
            # Estas acciones se deben ejecutar secuencialmente una a la vez,
            # y el juego no debe permitir interacción hasta que todas terminen

    def get_new_state(self):
        return self.checkpoints # La nueva lista de checkpoints actuales será lo que guardemos al salir del juego

    def get_entity(self, target):
        if target == 'game':
            return self.game
        elif target == 'inventory':
            return self.game.inventory
        elif target[0] == 'S':
            return None
        elif target[0] == 'C':
            for char in self.game.current_scene.characters:
                if char.id == target[2:]:
                    return char
        elif target[0] == 'O':
            for obj in self.game.current_scene.objects:
                if obj.id == target[2:]:
                    return obj
        print("NOT FOUND")