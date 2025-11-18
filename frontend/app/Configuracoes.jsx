import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import React, { useEffect, useRef } from 'react';
import {
  Animated,
  Image,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import Logofundo from "../assets/images/Logofundo.png";



const Configuracoes = React.memo(() => {
    const rout = useRouter();
  
    
    const goTo = (path) => {
      rout.push(`/${path}`);
    }
    
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const navigation = useNavigation();

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 600,
      useNativeDriver: true,
    }).start();
  }, [fadeAnim]);

  return (
    <LinearGradient colors={['#8000d5', '#f910a3', '#fddf00']} style={styles.gradient}>
      <SafeAreaView style={styles.safe}>
        {/* Botão de voltar */}
        <TouchableOpacity style={styles.voltar} onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={22} color="#fff" />
        </TouchableOpacity>

        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          <Animated.View style={[styles.container, { opacity: fadeAnim }]}>
            {/* Logo */}
            <View style={styles.logoContainer}>
              <Image
                style={styles.logo}
                source={Logofundo}
                accessibilityLabel="Logo do aplicativo"
              />
            </View>

            {/* Título */}
            <Text style={styles.titulo}>Configurações</Text>

            {/* Botões */}
            <View style={styles.botoesContainer} >
              <TouchableOpacity style={styles.botao}onPress={() => goTo('privacidade')}>
                <Text style={styles.textoBotao}>Privacidade</Text>
              </TouchableOpacity>

              <TouchableOpacity style={styles.botao}>
                <Text style={styles.textoBotao}>Aparência</Text>
              </TouchableOpacity>
            </View>
          </Animated.View>
        </ScrollView>
      </SafeAreaView>
    </LinearGradient>
  );
});

Configuracoes.displayName = 'Configuracoes';

const styles = StyleSheet.create({
  gradient: {
    flex: 1,
  },
  safe: {
    flex: 1,
  },
  voltar: {
    position: 'absolute',
    top: 55,
    left: 25,
    zIndex: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 25,
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  container: {
    alignItems: 'center',
    width: '100%',
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 15,
  },
  logo: {
    width: 120,
    height: 120,
    borderRadius: 25,
    backgroundColor: '#fff',
    resizeMode: 'contain',
  },
  logoTexto: {
    color: '#fff',
    fontSize: 18,
    marginTop: 8,
    fontFamily: 'negrito',
  },
  titulo: {
    fontFamily: 'negrito',
    color: '#fff',
    fontSize: 26,
    textAlign: 'center',
    marginVertical: 25,
  },
  botoesContainer: {
    width: '75%',
    alignItems: 'center',
    gap: 18,
  },
  botao: {
    width: '100%',
    paddingVertical: 12,
    borderRadius: 25,
    borderWidth: 2,
    borderColor: '#fff',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.15)',
  },
  textoBotao: {
    color: '#fff',
    fontSize: 18,
    fontFamily: 'negrito',
  },
});

export default Configuracoes;
