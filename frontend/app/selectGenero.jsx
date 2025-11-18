import React, { useState } from 'react';
import {
  Text,
  TouchableOpacity,
  StyleSheet,
  FlatList,
  SafeAreaView,
} from 'react-native';
import { AntDesign } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native"; 

const GENEROS = [
  'Funk', 'Sertanejo', 'Rap', 'Trap', 'Jerk', 'Drill',
  'Samba', 'Axé', 'Soul', 'Blues', 'Rock', 'Gospel',
];

const GeneroSelector = () => {
  const [selecionados, setSelecionados] = useState([]);
  const navigation = useNavigation(); 

  const toggleGenero = (genero) => {
    if (selecionados.includes(genero)) {
      setSelecionados(selecionados.filter((g) => g !== genero));
    } else {
      setSelecionados([...selecionados, genero]);
    }
  };

  const renderGenero = ({ item }) => {
    const isSelected = selecionados.includes(item);
    return (
      <TouchableOpacity
        onPress={() => toggleGenero(item)}
        style={[
          styles.generoBotao,
          isSelected && styles.generoBotaoSelecionado,
        ]}
      >
        <Text
          style={[
            styles.generoTexto,
            isSelected && styles.generoTextoSelecionado,
          ]}
        >
          {item}
        </Text>
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      
      <TouchableOpacity style={styles.backCircle} onPress={() => navigation.goBack()}>
        <AntDesign name="arrowleft" size={20} color="#fff" />
      </TouchableOpacity>

      <Text style={styles.titulo}>Selecione seus Gêneros Musicais Preferidos:</Text>

      <FlatList
        data={GENEROS}
        keyExtractor={(item) => item}
        renderItem={renderGenero}
        numColumns={3}
        contentContainerStyle={styles.lista}
      />

      <TouchableOpacity
        style={[
          styles.botaoContinuar,
          selecionados.length === 0 && styles.botaoDesativado,
        ]}
        disabled={selecionados.length === 0}
        onPress={() => console.log('Selecionados:', selecionados)}
      >
        <Text style={styles.textoContinuar}>Continuar</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  titulo: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  backCircle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "rgba(150, 47, 191, 0.8)",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 15,
  },
  lista: {
    gap: 10,
  },
  generoBotao: {
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#ccc',
    margin: 5,
  },
  generoBotaoSelecionado: {
    backgroundColor: '#962fbf',
    borderColor: '#962fbf',
  },
  generoTexto: {
    fontSize: 16,
    color: '#333',
  },
  generoTextoSelecionado: {
    color: '#fff',
    fontWeight: 'bold',
  },
  botaoContinuar: {
    backgroundColor: '#962fbf',
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 'auto',
  },
  botaoDesativado: {
    backgroundColor: '#ccc',
  },
  textoContinuar: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default GeneroSelector;
