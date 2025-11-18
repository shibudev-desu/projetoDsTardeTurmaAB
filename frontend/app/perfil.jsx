import { LinearGradient } from 'expo-linear-gradient';
import React, { useMemo, useState, memo, useCallback } from 'react';
import { Image, StyleSheet, Text, TouchableOpacity, useWindowDimensions, View } from 'react-native';
import { AntDesign } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native"; 

const ProfileScreen = memo(() => {
  const { width } = useWindowDimensions();
  const [pressingLogout, setPressingLogout] = useState(false);
   const navigation = useNavigation(); 

  
  const rf = useMemo(
    () => (size) =>
      Math.round(Math.max(size * 0.9, Math.min(size * 1.6, size * (width / 390)))),
    [width]
  );

  const isSmallScreen = width < 360;

 
  const statsData = useMemo(
    () => [
      { number: 0, label: 'Músicas Curtidas' },
      { number: 0, label: 'Artistas Descobertos' },
      { number: 0, label: 'Playlists Criadas' },
    ],
    []
  );

 
  const handlePressIn = useCallback(() => setPressingLogout(true), []);
  const handlePressOut = useCallback(() => setPressingLogout(false), []);

  return (
    <View style={styles.container}>
     
    
       <LinearGradient colors={['#8000d5', '#f910a3', '#fddf00']} style={styles.gradient}>
        <Image
          source={{ uri: 'https://cdn-icons-png.flaticon.com/512/149/149071.png' }}
          style={{
            width: rf(100),
            height: rf(100),
            borderRadius: rf(50),
            marginBottom: rf(5),
            borderWidth: 2,
            borderColor: '#fff',
          }}
          resizeMode="cover"
        />

        <View style={{ alignItems: 'center', gap: rf(3) }}>
          <Text style={[styles.username, { fontSize: rf(22 + (isSmallScreen ? -2 : 0)) }]}>Usuário</Text>
          <Text style={[styles.email, { fontSize: rf(13) }]}>0 seguidores - 4 seguindo</Text>
          <Text style={[styles.memberSince, { fontSize: rf(12) }]}>YRCAP     Naosouiphone</Text>
          <Text style={[styles.location, { fontSize: rf(13) }]}>São Paulo, SP</Text>
        </View>
      
      <TouchableOpacity style={styles.backCircle} onPress={() => navigation.goBack()}>
                <AntDesign name="arrowleft" size={20} color="#fff" />
              </TouchableOpacity>

     
      
      <View
        style={{
          flexDirection: 'row',
          justifyContent: 'center',
          marginTop: rf(35),
          gap: rf(30),
          flexWrap: 'wrap',
          width: '100%',
          paddingHorizontal: width * 0.1,
        }}
      >
        {statsData.map((item, i) => (
          <View key={i} style={{ alignItems: 'center', minWidth: rf(100) }}>
            <Text style={[styles.statNumber, { fontSize: rf(26) }]}>{item.number}</Text>
            <Text style={[styles.statLabel, { fontSize: rf(13) }]}>{item.label}</Text>
          </View>
        ))}
      </View>

     
      <TouchableOpacity
        activeOpacity={0.9}
        style={[
          styles.logoutButton,
          {
            backgroundColor: pressingLogout ? '#d99ac1' : '#F1A7D5',
            transform: [{ scale: pressingLogout ? 0.97 : 1 }],
            paddingVertical: rf(14),
            marginTop: rf(55),
            borderRadius: rf(14),
            width: width * 0.7,
            elevation: 3,
          },
        ]}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
      >
        <Text style={[styles.logoutText, { fontSize: rf(17) }]}>Sair da Conta</Text>
      </TouchableOpacity>
      

  
      <View style={styles.footer}>
        {['Player', 'Curtidas', 'Perfil'].map((label, i) => (
          <TouchableOpacity
            key={i}
            style={styles.footerItem}
            activeOpacity={0.8}
          >
            <Text style={styles.footerText}>{label}</Text>
          </TouchableOpacity>
        ))}
         
      </View>
      </LinearGradient>
    </View>
   
  );
});

ProfileScreen.displayName = 'ProfileScreen';

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#ffd3e8', alignItems: 'center' },
  header: {
    width: '80%',
    height: '80%',
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
    backCircle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "rgba(255,255,255,0.18)",
    alignItems: "center",
    justifyContent: "center",
    marginTop: 12,
    marginLeft: -2,
  },
  username: { 
    fontWeight: 'bold',
     color: '#441b34' 
    },
  email: { color: '#380d26' },
  memberSince: { color: '#2c2c2c' },
  location: { color: '#6b4b63' },
  statNumber: { fontWeight: 'bold', color: '#F1A7D5' },
  statLabel: { color: '#D9A6C4', textAlign: 'center' },
  logoutButton: { alignItems: 'center' },
  logoutText: { color: '#fff', fontWeight: 'bold' },
  
  
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 12,
    backgroundColor: '#f7e6f0',
    width: '100%',
    borderTopWidth: 1,
    borderTopColor: '#e5c7da',
  },
  footerItem: { padding: 10 },
  footerText: { fontSize: 14, fontWeight: 'bold', color: '#441b34' },
});

export default ProfileScreen;
