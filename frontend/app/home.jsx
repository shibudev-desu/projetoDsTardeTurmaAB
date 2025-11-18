import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View
} from 'react-native';

const App = () => {
  const rout = useRouter();

  
  const goTo = (path) => {
    rout.push(`/${path}`);
  };

  return (
    <LinearGradient
      colors={['#962fbf', '#d62976', '#fa7e1e', '#feda75', '#4f5bd5']}
      style={styles.container}
      start={{ x: 0.5, y: 0 }}
      end={{ x: 0.5, y: 1 }}
    >
      <SafeAreaView style={{ flex: 1 }}>
        <View style={styles.header}>
          <Text style={styles.headerText}>Bem Vindo!! </Text>
        </View>

        <View style={styles.fundoPost}>
          <View style={styles.postagem}>
            <Text style={styles.titulo}>Título da Postagem</Text>
            <Text style={styles.conteudo}>
              Este é o conteúdo da sua postagem. Você pode colocar texto, imagens ou qualquer outro componente aqui.
            </Text>
          </View>
          <View style={styles.postagem}>
            <Text style={styles.titulo}>Título da Postagem</Text>
            <Text style={styles.conteudo}>
              Este é o conteúdo da sua postagem. Você pode colocar texto, imagens ou qualquer outro componente aqui.
            </Text>
          </View>
          <View style={styles.postagem}>
            <Text style={styles.titulo}>Título da Postagem</Text>
            <Text style={styles.conteudo}>
              Este é o conteúdo da sua postagem. Você pode colocar texto, imagens ou qualquer outro componente aqui.
            </Text>
          </View>
        </View>

      
        <View style={styles.nav}>
          <TouchableOpacity style={styles.navItem} onPress={() => goTo('Configuracoes')}>
            <Text style={styles.navText1}>Configurações</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.navItem} onPress={() => goTo('avatarperfil')}>
            <Text style={styles.navText1}>Avatar-Perfil</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.navItem} onPress={() => goTo('home')}>
            <Text style={styles.navText1}>Home</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.navItem} onPress={() => goTo('curtidas')}>
            <Text style={styles.navText1}>Curtidas</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.navItem} onPress={() => goTo('perfil')}>
            <Text style={styles.navText1}>Perfil</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.navItem} onPress={() => goTo('selectGenero')}>
            <Text style={styles.navText1}>SelecionarGenero</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.navItem} onPress={() => goTo('Swipes')}>
            <Text style={styles.navText1}>Swipes</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.navItem} onPress={() => goTo('perfilartista')}>
            <Text style={styles.navText1}>PerfilArtista</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.navItem} onPress={() => goTo('uploadMusic')}>
            <Text style={styles.navText1}>UploadMusic</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
  },
  header: {
    padding: 20,
    alignItems: 'center',
    borderRadius: 10,
    marginBottom: 10,
  },
  headerText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  fundoPost: {
    height: 400,
  },
  postagem: {
    backgroundColor: 'rgba(128, 128, 128, 0.45)',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: 'white',
    padding: 16,
    width: '100%',
    maxWidth: 400,
    marginBottom: 10,
  },
  titulo: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  conteudo: {
    fontSize: 16,
    color: '#f0f0f0',
  },
  nav: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    backgroundColor: '#1d1436',
    borderRadius: 10,
    paddingVertical: 10,
    marginBottom: 2,
  },
  navItem: {
    padding: 10,
  },
  navText1: {
    fontSize: 16,
    color: '#ff3cf5',
  },
});

export default App;
