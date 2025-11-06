import { Text, TouchableOpacity, TextInput, View, StyleSheet, ScrollView } from "react-native";
import React, { useState } from 'react';
import { LinearGradient } from "expo-linear-gradient";
import { useNavigation } from "@react-navigation/native"; 

export default function Upload() {
  const navigation = useNavigation();
  const [selectedGenre, setSelectedGenre] = useState('');
  const [isGenreListVisible, setIsGenreListVisible] = useState(false);

  const genres = ['Pop', 'Rock', 'Hip Hop', 'Eletronic', 'Indie', 'Jaxx'];

  const handleSelectGenre = (genre) => {
    setSelectedGenre(genre);
    setIsGenreListVisible(false);
  };

  return (
    <LinearGradient
      colors={['#8000d5', '#f910a3', '#fddf00']}
      style={styles.container}
    >
      <ScrollView 
        style={styles.scrollContainer} 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{
          flexGrow: 1,
          justifyContent: 'center',
          alignItems: 'center',
          paddingVertical: 20
        }}
      >
        <View style={styles.header}>
          <TouchableOpacity 
            onPress={() => navigation.goBack()} 
            style={styles.backButton}
          >
            <Text style={styles.backArrow}>←</Text>
          </TouchableOpacity>

          <Text style={styles.title}>Upload de Música</Text>
          <Text style={styles.subtitle}>Compartilhe sua arte com o mundo</Text>
        </View>

        <View style={styles.form}>
         
          <View style={styles.inputBlock}>
            <Text style={styles.label}>Arquivo de Áudio</Text>
            <TouchableOpacity style={styles.uploadButton}>
              <Text style={styles.uploadButtonText}>📁 Selecionar Música</Text>
            </TouchableOpacity>
          </View>

         
          <View style={styles.inputBlock}>
            <Text style={styles.label}>Capa do Álbum</Text>
            <TouchableOpacity style={styles.uploadButton}>
              <Text style={styles.uploadButtonText}>🖼️ Selecionar Imagem</Text>
            </TouchableOpacity>
          </View>

          
          <View style={styles.inputBlock}>
            <Text style={styles.label}>Título da Música</Text>
            <TextInput style={styles.input} placeholder="Digite o título da música" placeholderTextColor="#aaa" />
          </View>

          
          <View style={styles.inputBlock}>
            <Text style={styles.label}>Artista</Text>
            <TextInput style={styles.input} placeholder="Seu nome artístico" placeholderTextColor="#aaa" />
          </View>

         
          <View style={styles.inputBlock}>
            <Text style={styles.label}>Álbum</Text>
            <TextInput style={styles.input} placeholder="Nome do álbum" placeholderTextColor="#aaa" />
          </View>

          
          <View style={styles.inputBlock}>
            <Text style={styles.label}>Gênero Musical</Text>
            <TouchableOpacity
              style={styles.selectButton}
              onPress={() => setIsGenreListVisible(!isGenreListVisible)}
            >
              <Text style={styles.selectButtonText}>
                {selectedGenre || 'Selecionar Gênero'}
              </Text>
              <Text style={styles.selectArrow}>▼</Text>
            </TouchableOpacity>

            {isGenreListVisible && (
              <View style={styles.genreList}>
                {genres.map((genre) => (
                  <TouchableOpacity
                    key={genre}
                    style={styles.genreItem}
                    onPress={() => handleSelectGenre(genre)}
                  >
                    <Text style={styles.genreText}>{genre}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            )}
          </View>

          
          <View style={styles.inputBlock}>
            <Text style={styles.label}>Descrição</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              placeholder="Conte sobre sua música..."
              placeholderTextColor="#aaa"
              multiline={true}
              numberOfLines={4}
            />
          </View>

          
          <TouchableOpacity style={styles.uploadFinalButton}>
            <Text style={styles.uploadFinalButtonText}>🎵 Fazer Upload</Text>
          </TouchableOpacity>

         
          <View style={styles.infoBox}>
            <Text style={styles.infoTitle}>📋 Informações Importantes:</Text>
            <Text style={styles.infoText}>• Formatos aceitos: MP3, WAV, FLAC</Text>
            <Text style={styles.infoText}>• Tamanho máximo: 50MB</Text>
            <Text style={styles.infoText}>• Capa: JPG, PNG (mín. 500x500px)</Text>
          </View>
        </View>
      </ScrollView>
    </LinearGradient>
  )
}

const styles = StyleSheet.create({
  container: { 
    flex: 1 
  },
  scrollContainer: { 
    flex: 1,
    paddingHorizontal: 24,
  },
  header: { 
    paddingTop: 60, 
    paddingBottom: 20,
    width: '100%',
    alignItems: 'center'
  },
  backButton: { 
    position: 'absolute',
    left: 10,
    top: 10,
    zIndex: 1
  },
  backArrow: { 
    fontSize: 24, 
    color: "#FFF" 
  },
  inputBlock: { 
    marginBottom: 20 
  },
  label: { 
    fontSize: 16, 
    color: "#FFF", 
    marginBottom: 8,
    fontFamily: "normal" 
  },
  form: { 
    width: '90%',
    maxWidth: 450,
    paddingBottom: 40,
    alignItems: 'center'
  },
  input: {
    borderRadius: 25,
    fontSize: 20,
    borderWidth: 2,
    borderColor: "#FFF",
    textAlign: "center",
    fontFamily: "normal",
    color: "#FFF",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 7 },
    shadowRadius: 4,
    elevation: 5,
    margin: 10,
    backgroundColor: "#1D143642",
    minHeight: 70,
    height: 70,
    paddingVertical: 10,
    paddingHorizontal: 15,
    textAlignVertical: 'center',
  },
  textArea: { 
    height: 120, 
    paddingTop: 12, 
    textAlignVertical: "top",
    textAlign: "left"
  },
  uploadButton: {
    borderRadius: 25,
    borderWidth: 2,
    borderColor: "#FFF",
    paddingVertical: 15,
    paddingHorizontal: 16,
    alignItems: "center",
    backgroundColor: "#1D143642",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 7 },
    shadowRadius: 4,
    elevation: 5,
    margin: 10,
  },
  uploadButtonText: { 
    fontSize: 18, 
    color: "#FFF",
    fontFamily: "normal"
  },
  selectButton: {
    borderRadius: 25,
    borderWidth: 2,
    borderColor: "#FFF",
    paddingVertical: 15,
    paddingHorizontal: 16,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#1D143642",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 7 },
    shadowRadius: 4,
    elevation: 5,
    margin: 10,
  },
  selectButtonText: { 
    fontSize: 18, 
    color: "#FFF",
    fontFamily: "normal"
  },
  selectArrow: { 
    fontSize: 14, 
    color: "#FFF" 
  },
  genreList: { 
    marginTop: 10, 
    backgroundColor: "#1D143642", 
    borderRadius: 25,
    borderWidth: 2,
    borderColor: "#FFF",
  },
  genreItem: { 
    padding: 12, 
    borderBottomWidth: 1, 
    borderBottomColor: "rgba(255,255,255,0.3)" 
  },
  genreText: { 
    fontSize: 16, 
    color: "#FFF",
    textAlign: "center",
    fontFamily: "normal"
  },
  uploadFinalButton: {
    height: 70,
    backgroundColor: '#1d1436',
    borderColor: '#8000D5',
    alignItems: 'center',
    textAlign: 'center',
    borderRadius: 40,
    marginTop: 20,
    marginBottom: 30,
    justifyContent: 'center'
  },
  uploadFinalButtonText: { 
    color: '#FFF', 
    fontFamily: 'negrito',
    fontSize: 19
  },
  title: { 
    fontSize: 26, 
    color: "#FFF", 
    textAlign: "center", 
    marginBottom: 8,
    fontFamily: "negrito"
  },
  subtitle: { 
    fontSize: 16, 
    color: "#FFF", 
    textAlign: "center",
    fontFamily: "normal",
    marginBottom: 20
  },
  infoBox: { 
    backgroundColor: "#1D143642", 
    borderRadius: 25, 
    padding: 20, 
    marginTop: 10,
    borderWidth: 2,
    borderColor: "#FFF", 
  },
  infoTitle: { 
    fontSize: 18, 
    color: "#FFF", 
    marginBottom: 10,
    fontFamily: "negrito"
  },
  infoText: { 
    fontSize: 16, 
    color: "#FFF", 
    marginBottom: 5,
    fontFamily: "normal"
  },
});
