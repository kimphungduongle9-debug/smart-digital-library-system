import React, { useEffect, useState } from "react";
import { View, FlatList, Text } from "react-native";
import { Card, Searchbar, ActivityIndicator } from "react-native-paper";
import Apis, { endpoints } from "../../configs/Apis";
import Styles from "./Styles";

export default function Home() {
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(false);
    const [q, setQ] = useState("");

    const loadDocuments = async () => {
        try {
            setLoading(true);
            let url = endpoints.documents;

            if (q) {
                url = `${url}?search=${q}`;
            }

            let res = await Apis.get(url);

            if (res.data.results) {
                setDocuments(res.data.results);
            } else {
                setDocuments(res.data);
            }
        } catch (ex) {
            console.log(ex);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadDocuments();
    }, []);

    return (
        <View style={Styles.container}>
            <Searchbar
                placeholder="Tìm tài liệu theo tên, tác giả..."
                value={q}
                onChangeText={setQ}
                onSubmitEditing={loadDocuments}
                style={Styles.search}
            />

            {loading && <ActivityIndicator animating={true} />}

            <FlatList
                data={documents}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                    <Card style={Styles.card}>
                        <Card.Title
                            title={item.title}
                            subtitle={`${item.author} - ${item.published_year}`}
                        />
                        <Card.Content>
                            <Text>{item.description}</Text>
                            <Text>Chuyên ngành: {item.category_detail?.name}</Text>
                            <Text>Giá: {item.price} VNĐ</Text>
                            <Text>Độ phổ biến: {item.popularity}</Text>
                        </Card.Content>
                    </Card>
                )}
            />
        </View>
    );
}