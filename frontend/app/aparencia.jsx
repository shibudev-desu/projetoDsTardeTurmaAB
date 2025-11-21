import { Text, TouchableOpacity, View } from "react-native";





export default function HomeScreen() {
  return (
    <View>
      <Text>Aparência</Text>

      <TouchableOpacity>
        <Text>Amarelo</Text>
      </TouchableOpacity>
      <TouchableOpacity>
        <Text>Vermelho</Text>
      </TouchableOpacity>
      <TouchableOpacity>
        <Text>Roxo</Text>
      </TouchableOpacity>
    </View>
  );
}

